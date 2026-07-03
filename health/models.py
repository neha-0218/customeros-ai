from django.db import models
from core.base_models import BaseModel
from accounts.models import CustomerAccount, User


class HealthScoreSnapshot(BaseModel):
    """
    A point-in-time health score for a customer account.

    One row per calculation run (e.g. daily batch job), not a single
    mutable field on CustomerAccount. This is deliberate: without
    history, we can't show a health trend, calculate time-to-risk-detection,
    or validate whether the churn prediction model actually works over time.

    Component scores are stored individually (not just the composite)
    so the AI Copilot can later explain WHY a score dropped —
    e.g. "ticket volume spiked" vs "feature adoption fell" — rather
    than just reporting a number with no explanation.
    """

    customer_account = models.ForeignKey(
        CustomerAccount,
        on_delete=models.CASCADE,
        related_name='health_snapshots'
    )

    composite_score = models.FloatField(
        help_text="0-100 overall health score"
    )

    # Component scores — what makes up the composite.
    # Storing these separately enables explainability, not just a black-box number.
    usage_score = models.FloatField(default=0, help_text="0-100, based on product usage frequency")
    ticket_score = models.FloatField(default=0, help_text="0-100, inverse of ticket volume/severity")
    sentiment_score = models.FloatField(default=0, help_text="0-100, derived from feedback sentiment")
    adoption_score = models.FloatField(default=0, help_text="0-100, % of available features used")
    payment_score = models.FloatField(default=0, help_text="0-100, based on payment/billing status")

    risk_tier = models.CharField(
        max_length=20,
        choices=[
            ('healthy', 'Healthy'),
            ('moderate', 'Moderate Risk'),
            ('at_risk', 'At Risk'),
            ('critical', 'Critical'),
        ],
        default='healthy'
    )

    calculation_method = models.CharField(
        max_length=50,
        default='rule_based',
        help_text="'rule_based' for now; will support 'ml_model' once churn prediction (Phase 14) is live"
    )

    def __str__(self):
        return f"{self.customer_account.name} — {self.composite_score} ({self.risk_tier})"

    class Meta:
        ordering = ['-created_at']


class RiskFlag(BaseModel):
    """
    Created when an account's health score crosses below a risk threshold.
    Tracks the full lifecycle: flagged -> investigated -> intervened -> resolved.

    This directly supports the 'Time to Risk Detection' metric from your
    metrics dictionary: resolved_at - created_at on the intervention,
    compared against when the triggering snapshot was created.
    """

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('investigating', 'Investigating'),
        ('intervention_logged', 'Intervention Logged'),
        ('resolved', 'Resolved'),
        ('churned', 'Churned'),
    ]

    customer_account = models.ForeignKey(
        CustomerAccount,
        on_delete=models.CASCADE,
        related_name='risk_flags'
    )
    triggering_snapshot = models.ForeignKey(
        HealthScoreSnapshot,
        on_delete=models.SET_NULL,
        null=True,
        related_name='risk_flags'
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='open')
    trigger_reason = models.CharField(
        max_length=255,
        help_text="e.g. 'composite_score below 40' or 'ticket_score dropped sharply'"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_risk_flags'
    )

    intervention_notes = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer_account.name} — {self.status} ({self.trigger_reason})"

    @property
    def days_open(self):
        """Used for the Time to Risk Detection metric."""
        from django.utils import timezone
        end = self.resolved_at or timezone.now()
        return (end - self.created_at).days