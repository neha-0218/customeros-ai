from django.db import models
from core.base_models import BaseModel
from accounts.models import User


class RoadmapItem(BaseModel):
    """
    A planned, scheduled product commitment — distinct from Feature.

    A Feature is a raw request from a customer. A RoadmapItem is what
    the PM has decided to actually build, potentially aggregating
    multiple related Features into one initiative. Keeping these as
    separate models reflects the real PM workflow: many requests become
    one roadmap decision.
    """

    STATUS_CHOICES = [
        ('backlog', 'Backlog'),
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    ]

    QUARTER_CHOICES = [
        ('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('Q4', 'Q4'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='backlog')

    priority_score = models.FloatField(
        default=0,
        help_text="Composite priority score — populated by AI Prioritization Assistant (Phase 17)"
    )

    linked_features = models.ManyToManyField(
        'features.Feature',
        blank=True,
        related_name='roadmap_items',
        help_text="Raw feature requests this roadmap item addresses"
    )

    target_quarter = models.CharField(max_length=10, choices=QUARTER_CHOICES, blank=True)
    target_year = models.IntegerField(null=True, blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_roadmap_items'
    )

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        ordering = ['-priority_score']