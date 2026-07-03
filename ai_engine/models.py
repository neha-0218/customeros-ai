from django.db import models
from core.base_models import BaseModel
from accounts.models import User, CustomerAccount


class AIInsight(BaseModel):
    """
    A persisted AI-generated insight — the core object behind
    ai_insight_generated / viewed / accepted / rejected / regenerated
    events from the taxonomy.

    Storing insights (not just returning them live from an API call)
    matters because:
    1. AI Evaluation Framework (Phase 20) needs historical acceptance
       rate data — can't measure what you don't store
    2. PMs need to revisit past insights, not just see them once and lose them
    3. Audit trail for "what did the AI recommend and did we act on it"
       directly supports Decision Velocity tracking
    """

    INSIGHT_TYPE_CHOICES = [
        ('feedback_theme', 'Feedback Theme Analysis'),
        ('churn_risk', 'Churn Risk Explanation'),
        ('prioritization', 'Feature Prioritization Recommendation'),
        ('copilot_answer', 'AI Copilot Q&A Response'),
        ('roadmap_suggestion', 'Roadmap Suggestion'),
    ]

    STATUS_CHOICES = [
        ('generated', 'Generated'),
        ('viewed', 'Viewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('regenerated', 'Regenerated'),
    ]

    insight_type = models.CharField(max_length=30, choices=INSIGHT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='generated')

    customer_account = models.ForeignKey(
        CustomerAccount,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ai_insights',
        help_text="Null for org-wide insights not tied to a specific account"
    )
    generated_for_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ai_insights'
    )

    prompt_input = models.TextField(help_text="What was sent to the AI — for debugging and prompt iteration")
    response_text = models.TextField(help_text="The AI's generated insight")

    model_used = models.CharField(max_length=100, help_text="e.g. 'meta-llama/llama-3-8b' via OpenRouter")
    latency_ms = models.IntegerField(null=True, blank=True)

    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return f"{self.insight_type} — {self.status} ({self.created_at.date()})"

    class Meta:
        ordering = ['-created_at']


class AIQuery(BaseModel):
    """
    A natural-language question asked via the AI Analytics Chat (RAG, Phase 19).
    Separate from AIInsight because a query is user-initiated input;
    an insight can be either proactively generated or query-triggered.
    The resulting AIInsight (if any) links back via response_insight.
    """

    asked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_queries')
    query_text = models.TextField()
    response_insight = models.ForeignKey(
        AIInsight,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='source_query'
    )

    def __str__(self):
        return self.query_text[:75]