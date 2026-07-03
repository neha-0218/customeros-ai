from django.db import models
from core.base_models import BaseModel
from accounts.models import CustomerAccount, User


class UsageEvent(BaseModel):
    """
    Raw product usage event, ingested from Mixpanel or logged manually.

    This is intentionally a thin, generic event log — not a separate
    model per event type. Real analytics platforms (Mixpanel, Amplitude)
    use exactly this pattern: one wide event table with a name + properties
    blob, not hundreds of rigid tables. This keeps ingestion flexible
    as our event taxonomy grows without needing new migrations per event.
    """

    customer_account = models.ForeignKey(
        CustomerAccount,
        on_delete=models.CASCADE,
        related_name='usage_events'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usage_events',
        help_text="Which user at the customer account triggered this event, if known"
    )

    event_name = models.CharField(
        max_length=100,
        help_text="e.g. 'feature_request_created', 'dashboard_viewed' — matches event taxonomy"
    )
    properties = models.JSONField(
        default=dict,
        blank=True,
        help_text="Event-specific properties as defined in the event taxonomy"
    )

    source = models.CharField(
        max_length=20,
        choices=[('mixpanel', 'Mixpanel'), ('manual', 'Manual'), ('internal', 'Internal Tracking')],
        default='internal'
    )

    def __str__(self):
        return f"{self.event_name} — {self.customer_account.name}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_name', 'created_at']),
            models.Index(fields=['customer_account', 'event_name']),
        ]