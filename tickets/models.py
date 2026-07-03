from django.db import models
from django.utils import timezone
from core.base_models import BaseModel
from accounts.models import CustomerAccount, User


class Ticket(BaseModel):
    """
    A support ticket raised by or about a customer account.

    Tickets are operational signals — distinct from Feedback (soft, qualitative)
    because they represent something broken or blocking, with real
    resolution-time SLAs attached.
    """

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    CATEGORY_CHOICES = [
        ('bug', 'Bug'),
        ('how_to', 'How-To Question'),
        ('feature_gap', 'Feature Gap'),
        ('billing', 'Billing'),
        ('performance', 'Performance'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
    ]

    customer_account = models.ForeignKey(
        CustomerAccount,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    # Forward reference to features.Feature — that app doesn't exist yet.
    # String reference lets Django resolve this once we build it.
    linked_feature = models.ForeignKey(
        'features.Feature',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_tickets'
    )

    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.priority.upper()}] {self.subject}"

    @property
    def resolution_time_hours(self):
        """
        Calculated, not stored — always accurate, never goes stale.
        Returns None if not yet resolved.
        """
        if self.resolved_at:
            delta = self.resolved_at - self.created_at
            return round(delta.total_seconds() / 3600, 2)
        return None

    @property
    def is_overdue(self):
        """
        Simple SLA check: critical tickets unresolved after 4 hours,
        high after 24 hours, are considered overdue.
        This is a placeholder rule — real SLA config would live in
        Organization settings, not hardcoded. Flagging this as a
        known simplification for now.
        """
        if self.status == 'resolved':
            return False
        hours_open = (timezone.now() - self.created_at).total_seconds() / 3600
        sla_hours = {'critical': 4, 'high': 24, 'medium': 72, 'low': 168}
        return hours_open > sla_hours.get(self.priority, 168)
        