from django.db import models
from core.base_models import BaseModel
from accounts.models import Organization


class IntegrationConfig(BaseModel):
    """
    Stores connection config per Organization for external tools
    (Jira, Mixpanel). API keys should ideally be encrypted at rest
    in a real production system — flagging this as a known
    simplification for portfolio scope. Don't store real production
    credentials here as-is.
    """

    PROVIDER_CHOICES = [
        ('jira', 'Jira'),
        ('mixpanel', 'Mixpanel'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='integrations')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    api_key = models.CharField(max_length=500, blank=True)
    config = models.JSONField(default=dict, blank=True, help_text="Provider-specific settings, e.g. Jira project key")
    is_active = models.BooleanField(default=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.organization.name} — {self.provider}"

    class Meta:
        unique_together = ['organization', 'provider']