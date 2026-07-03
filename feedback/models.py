from django.db import models
from core.base_models import BaseModel
from accounts.models import CustomerAccount, User


class Feedback(BaseModel):
    """
    A single piece of customer feedback — the raw signal that everything
    downstream (AI analysis, health scoring, feature requests) is built on.

    sentiment_score and urgency_score are null at creation. They get
    populated later by the AI Feedback Intelligence engine (Phase 15).
    We do NOT calculate these here — keeping ingestion and analysis
    as separate concerns means we can re-run AI analysis later without
    touching the raw feedback record.
    """

    SOURCE_CHOICES = [
        ('survey', 'In-App Survey'),
        ('support_ticket', 'Support Ticket'),
        ('sales_call', 'Sales Call Notes'),
        ('email', 'Email'),
        ('manual', 'Manually Entered'),
        ('nps', 'NPS Response'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewed', 'Reviewed'),
        ('linked', 'Linked to Feature'),
        ('archived', 'Archived'),
    ]

    customer_account = models.ForeignKey(
        CustomerAccount,
        on_delete=models.CASCADE,
        related_name='feedback_items'
    )
    submitted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='submitted_feedback',
        help_text="Internal user who logged this feedback, if applicable"
    )
    content = models.TextField(help_text="The raw feedback text")
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='manual')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # Populated later by AI engine — nullable by design
    sentiment_score = models.FloatField(
        null=True, blank=True,
        help_text="-1.0 (very negative) to 1.0 (very positive). Set by AI engine."
    )
    urgency_score = models.FloatField(
        null=True, blank=True,
        help_text="0.0 to 1.0. Set by AI engine."
    )

    def __str__(self):
        return f"{self.customer_account.name} — {self.content[:50]}"


class FeedbackTheme(BaseModel):
    """
    AI-generated theme/category extracted from feedback content
    (e.g. "pricing complaint", "onboarding friction", "missing integration").

    Separate model, not a CharField on Feedback, because:
    - One feedback item can have multiple themes
    - Themes need to be aggregated across feedback for the AI Copilot
      to answer "what are the top 3 themes this month"
    """
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name='themes'
    )
    theme_name = models.CharField(max_length=100)
    confidence_score = models.FloatField(
        default=0.0,
        help_text="AI confidence in this theme assignment, 0.0 to 1.0"
    )

    def __str__(self):
        return f"{self.theme_name} ({self.feedback_id})"