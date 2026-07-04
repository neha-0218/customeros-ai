import requests
import json
import time
from django.conf import settings
from django.db.models import Count


OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


def call_openrouter(prompt: str, system_prompt: str = None) -> tuple[str, int]:
    """
    Makes a single call to OpenRouter API.
    Returns (response_text, latency_ms).
    Raises ValueError on API failure so callers can handle gracefully.
    """
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://customeros-ai.com",
        "X-Title": "CustomerOS AI",
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.3,
    }

    start = time.time()
    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        latency_ms = int((time.time() - start) * 1000)

        if response.status_code != 200:
            raise ValueError(f"OpenRouter error {response.status_code}: {response.text}")

        data = response.json()
        text = data['choices'][0]['message']['content'].strip()
        return text, latency_ms

    except requests.exceptions.Timeout:
        raise ValueError("OpenRouter API timed out after 30 seconds")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"OpenRouter request failed: {str(e)}")


def generate_churn_risk_insight(account, snapshot):
    """
    Generates a churn risk explanation for a specific account.
    Input: CustomerAccount + latest HealthScoreSnapshot
    Output: AIInsight record
    """
    from ai_engine.models import AIInsight

    # Build context from real data
    recent_tickets = account.tickets.filter(
        status__in=['open', 'in_progress', 'escalated']
    ).order_by('-created_at')[:5]

    recent_feedback = account.feedback_items.order_by('-created_at')[:5]

    ticket_summary = "\n".join([
        f"- [{t.priority}] {t.subject} ({t.get_status_display()})"
        for t in recent_tickets
    ]) or "No open tickets"

    feedback_summary = "\n".join([
        f"- {f.content[:100]} (sentiment: {f.sentiment_score})"
        for f in recent_feedback
    ]) or "No recent feedback"

    system_prompt = """You are an AI product analyst for a B2B SaaS company.
Your job is to analyze customer health data and generate clear, actionable churn risk summaries.
Be specific. Use the data provided. Do not invent information not in the context.
Keep responses under 200 words. Structure with: Risk Level, Key Drivers, Recommended Action."""

    prompt = f"""Analyze churn risk for this customer account:

Account: {account.name}
Plan: {account.get_plan_tier_display()}
MRR: ${account.mrr}

Health Scores:
- Overall: {snapshot.composite_score}/100
- Usage: {snapshot.usage_score}/100
- Support Tickets: {snapshot.ticket_score}/100
- Sentiment: {snapshot.sentiment_score}/100
- Feature Adoption: {snapshot.adoption_score}/100
- Payment: {snapshot.payment_score}/100
Risk Tier: {snapshot.get_risk_tier_display()}

Open Tickets:
{ticket_summary}

Recent Feedback:
{feedback_summary}

Generate a churn risk summary with:
1. Risk Level (Critical/High/Medium/Low)
2. Top 3 churn drivers from the data
3. Specific recommended action with timeline"""

    try:
        response_text, latency_ms = call_openrouter(prompt, system_prompt)

        insight = AIInsight.objects.create(
            insight_type='churn_risk',
            status='generated',
            customer_account=account,
            generated_for_user=None,
            prompt_input=prompt,
            response_text=response_text,
            model_used=settings.OPENROUTER_MODEL,
            latency_ms=latency_ms,
        )
        return insight

    except ValueError as e:
        raise ValueError(f"Churn insight generation failed: {str(e)}")


def generate_feature_demand_insight(organization):
    """
    Analyzes feature requests + feedback + tickets to identify
    top product opportunities across the entire organization.
    """
    from ai_engine.models import AIInsight
    from features.models import Feature
    from feedback.models import FeedbackTheme

    top_features = Feature.objects.filter(
        organization_account__organization=organization
    ).order_by('-vote_count')[:8]

    top_themes = FeedbackTheme.objects.filter(
        feedback__customer_account__organization=organization
    ).values('theme_name').annotate(
        count=Count('id')
    ).order_by('-count')[:6]

    feature_summary = "\n".join([
        f"- {f.title}: {f.vote_count} votes, status: {f.get_status_display()}"
        for f in top_features
    ])

    theme_summary = "\n".join([
        f"- {t['theme_name']}: {t['count']} occurrences"
        for t in top_themes
    ])

    system_prompt = """You are an AI product analyst.
Analyze feature demand signals and generate prioritization recommendations.
Be specific and data-driven. Under 250 words.
Structure: Top Opportunities, Prioritization Recommendation, Risk if Ignored."""

    prompt = f"""Analyze product demand signals for this B2B SaaS organization:

Top Feature Requests by Votes:
{feature_summary}

Top Feedback Themes:
{theme_summary}

Generate:
1. Top 3 product opportunities based on demand signals
2. Which feature should be prioritized next and why
3. What risk exists if top demand signals are ignored"""

    try:
        response_text, latency_ms = call_openrouter(prompt, system_prompt)

        insight = AIInsight.objects.create(
            insight_type='prioritization',
            status='generated',
            customer_account=None,
            generated_for_user=None,
            prompt_input=prompt,
            response_text=response_text,
            model_used=settings.OPENROUTER_MODEL,
            latency_ms=latency_ms,
        )
        return insight

    except ValueError as e:
        raise ValueError(f"Feature demand insight failed: {str(e)}")


def generate_feedback_theme_insight(organization):
    """
    Analyzes recent feedback to surface dominant pain points and themes.
    """
    from ai_engine.models import AIInsight
    from feedback.models import Feedback

    recent_feedback = Feedback.objects.filter(
        customer_account__organization=organization
    ).order_by('-created_at')[:20]

    feedback_text = "\n".join([
        f"- [{f.get_source_display()}] {f.content[:120]} "
        f"(sentiment: {f.sentiment_score}, urgency: {f.urgency_score})"
        for f in recent_feedback
    ])

    system_prompt = """You are an AI product analyst specializing in customer feedback analysis.
Identify patterns, pain points, and actionable themes from customer feedback.
Under 250 words. Structure: Top Pain Points, Emerging Themes, Recommended Product Actions."""

    prompt = f"""Analyze these recent customer feedback items:

{feedback_text}

Generate:
1. Top 3 pain points appearing most frequently
2. Emerging themes that may not be on the roadmap yet
3. Specific product actions recommended based on this feedback"""

    try:
        response_text, latency_ms = call_openrouter(prompt, system_prompt)

        insight = AIInsight.objects.create(
            insight_type='feedback_theme',
            status='generated',
            customer_account=None,
            generated_for_user=None,
            prompt_input=prompt,
            response_text=response_text,
            model_used=settings.OPENROUTER_MODEL,
            latency_ms=latency_ms,
        )
        return insight

    except ValueError as e:
        raise ValueError(f"Feedback theme insight failed: {str(e)}")

def generate_copilot_response(question: str, user) -> 'AIInsight':
    """
    AI Copilot: answers natural language product questions
    grounded in real database context.

    This is structured retrieval + LLM generation.
    Not vector RAG yet — that's a planned enhancement.
    Current approach: detect question intent, pull relevant
    data, build context, generate grounded answer.
    """
    from ai_engine.models import AIInsight, AIQuery
    from accounts.models import CustomerAccount
    from feedback.models import Feedback, FeedbackTheme
    from tickets.models import Ticket
    from features.models import Feature
    from health.models import HealthScoreSnapshot, RiskFlag
    from django.db.models import Count, Avg

    org = user.organization
    question_lower = question.lower()

    # --- Build context based on question intent ---
    context_sections = []

    # Always include health summary
    accounts = CustomerAccount.objects.filter(
        organization=org, is_active=True
    ).prefetch_related('health_snapshots')

    at_risk_accounts = []
    for account in accounts:
        latest = account.health_snapshots.order_by('-created_at').first()
        if latest and latest.risk_tier in ['at_risk', 'critical']:
            at_risk_accounts.append(
                f"- {account.name}: score {latest.composite_score}, "
                f"tier {latest.get_risk_tier_display()}, "
                f"MRR ${account.mrr}"
            )

    if at_risk_accounts:
        context_sections.append(
            "AT-RISK ACCOUNTS:\n" + "\n".join(at_risk_accounts)
        )

    # Add ticket context if question is about support/problems
    if any(word in question_lower for word in
           ['ticket', 'support', 'issue', 'problem', 'bug', 'complaint']):
        open_tickets = Ticket.objects.filter(
            customer_account__organization=org,
            status__in=['open', 'in_progress', 'escalated']
        ).order_by('-created_at')[:10]

        ticket_lines = [
            f"- [{t.priority}] {t.subject} — {t.customer_account.name}"
            for t in open_tickets
        ]
        context_sections.append(
            "OPEN TICKETS:\n" + "\n".join(ticket_lines)
        )

    # Add feedback context if question is about sentiment/complaints
    if any(word in question_lower for word in
           ['feedback', 'complaint', 'sentiment', 'customers saying',
            'pain', 'frustrat']):
        themes = FeedbackTheme.objects.filter(
            feedback__customer_account__organization=org
        ).values('theme_name').annotate(
            count=Count('id')
        ).order_by('-count')[:8]

        theme_lines = [
            f"- {t['theme_name']}: {t['count']} occurrences"
            for t in themes
        ]

        recent_negative = Feedback.objects.filter(
            customer_account__organization=org,
            sentiment_score__lt=-0.3
        ).order_by('-urgency_score')[:5]

        neg_lines = [
            f"- {f.customer_account.name}: {f.content[:100]}"
            for f in recent_negative
        ]

        context_sections.append(
            "TOP FEEDBACK THEMES:\n" + "\n".join(theme_lines)
        )
        if neg_lines:
            context_sections.append(
                "HIGH-URGENCY NEGATIVE FEEDBACK:\n" + "\n".join(neg_lines)
            )

    # Add feature context if question is about prioritization/roadmap
    if any(word in question_lower for word in
           ['priorit', 'feature', 'build', 'roadmap', 'next',
            'focus', 'ship']):
        top_features = Feature.objects.filter(
            organization_account__organization=org
        ).order_by('-vote_count')[:8]

        feature_lines = [
            f"- {f.title}: {f.vote_count} votes, status: {f.get_status_display()}"
            for f in top_features
        ]
        context_sections.append(
            "TOP FEATURE REQUESTS:\n" + "\n".join(feature_lines)
        )

    # Add churn/risk context if question is about churn
    if any(word in question_lower for word in
           ['churn', 'risk', 'renew', 'cancel', 'lose', 'retain']):
        open_flags = RiskFlag.objects.filter(
            customer_account__organization=org,
            status__in=['open', 'investigating']
        ).select_related('customer_account')[:10]

        flag_lines = [
            f"- {f.customer_account.name}: {f.trigger_reason} "
            f"({f.days_open} days open)"
            for f in open_flags
        ]
        if flag_lines:
            context_sections.append(
                "OPEN RISK FLAGS:\n" + "\n".join(flag_lines)
            )

    # Build final context
    full_context = "\n\n".join(context_sections) if context_sections else \
        "No specific data context available for this question."

    system_prompt = """You are an AI Product Copilot for a B2B SaaS company.
You answer product and customer intelligence questions for Product Managers.
You have access to real customer data including health scores, tickets,
feedback, and feature requests.
Be specific and data-driven. Reference actual account names and numbers
from the context when relevant.
Keep answers under 300 words. Be direct and actionable.
Format with clear sections if the answer has multiple parts."""

    prompt = f"""Context from CustomerOS AI database:

{full_context}

Product Manager's question: {question}

Provide a specific, data-grounded answer based on the context above."""

    try:
        response_text, latency_ms = call_openrouter(prompt, system_prompt)

        # Store the query
        query = AIQuery.objects.create(
            asked_by=user,
            query_text=question,
        )

        # Store the insight
        insight = AIInsight.objects.create(
            insight_type='copilot_answer',
            status='generated',
            customer_account=None,
            generated_for_user=user,
            prompt_input=prompt,
            response_text=response_text,
            model_used=settings.OPENROUTER_MODEL,
            latency_ms=latency_ms,
        )

        # Link query to insight
        query.response_insight = insight
        query.save()

        return insight

    except ValueError as e:
        raise ValueError(f"Copilot response failed: {str(e)}")
