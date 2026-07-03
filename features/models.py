from django.db import models
from core.base_models import BaseModel
from accounts.models import CustomerAccount, User


class Feature(BaseModel):
    """
    A feature request. Minimal version for now — full prioritization
    fields (AI priority score, demand weighting, etc.) get added in
    Phase 10 when we build the Feature Prioritization Engine.

    Built now, ahead of schedule, because Ticket.linked_feature requires
    this model to exist. This is a known dependency, not scope creep —
    we're adding only what's needed to unblock tickets.
    """

    STATUS_CHOICES = [
        ('proposed', 'Proposed'),
        ('under_review', 'Under Review'),
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('shipped', 'Shipped'),
        ('declined', 'Declined'),
    ]

    organization_account = models.ForeignKey(
        CustomerAccount,
        on_delete=models.CASCADE,
        related_name='feature_requests',
        help_text="The customer account that originated this request"
    )
    requested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requested_features'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='proposed')
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title