from django.db import models
from core.base_models import BaseModel


class BusinessMetricSnapshot(BaseModel):
    """
    Periodic snapshot of business-level metrics (NOT infra metrics —
    those belong in Prometheus only, never duplicated into Postgres).

    This exists specifically to feed the Grafana 'Executive Product Health'
    and 'AI Health' dashboards with business context Prometheus can't
    derive on its own, e.g. Decision Velocity, AI Acceptance Rate.
    """

    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.metric_name}: {self.metric_value} ({self.created_at.date()})"

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['metric_name', 'created_at'])]