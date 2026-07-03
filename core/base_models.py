import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model used by every model in CustomerOS AI.

    Why UUID instead of auto-increment ID:
    - Prevents ID-guessing / enumeration attacks
    - Safe to expose in URLs and APIs
    - Plays well with external system IDs (Jira, Mixpanel) which aren't sequential ints

    Why created_at / updated_at on every model:
    - Required for nearly every metric in our dictionary (time to risk detection,
      decision velocity, resolution time, etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True