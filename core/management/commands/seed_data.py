import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import Organization, User, CustomerAccount
from feedback.models import Feedback, FeedbackTheme
from tickets.models import Ticket
from features.models import Feature
from health.models import HealthScoreSnapshot, RiskFlag
from analytics.models import UsageEvent
from roadmap.models import RoadmapItem
from ai_engine.models import AIInsight, AIQuery
from integrations.models import IntegrationConfig
from observability.models import BusinessMetricSnapshot


COMPANY_NAMES = [
    "Globex Corp", "Initech", "Umbrella Industries", "Stark Logistics", "Wayne Analytics",
    "Wonka Software", "Soylent Systems", "Hooli Inc", "Vandelay Industries", "Acme Tools",
    "Cyberdyne Systems", "Tyrell Corp", "Massive Dynamic", "Aperture Labs", "Pied Piper",
    "Dunder Mifflin", "Gringotts FinTech", "Oscorp Digital", "LexCorp Cloud", "Bluth Company"
]

FEEDBACK_SAMPLES = [
    "The onboarding flow is confusing, took us 3 days to get our team set up.",
    "Love the new dashboard, but loading times are slow with large datasets.",
    "We need a Salesforce integration, it's a dealbreaker for renewal.",
    "Support responded within minutes, great experience.",
    "Pricing feels steep compared to competitors for the features we use.",
    "The mobile app crashes whenever I try to export a report.",
    "Would like more granular permission controls for our admin users.",
    "API documentation is outdated, caused integration delays on our end.",
    "The new analytics view is exactly what we needed, well done.",
    "Billing was charged incorrectly twice this quarter, very frustrating.",
]

TICKET_SUBJECTS = [
    ("Cannot export CSV reports", "bug", "high"),
    ("How do I add a new team member?", "how_to", "low"),
    ("Need bulk import for customer data", "feature_gap", "medium"),
    ("Invoice shows wrong amount", "billing", "high"),
    ("Dashboard takes 30s to load", "performance", "critical"),
    ("SSO login fails intermittently", "bug", "critical"),
    ("Request for dark mode", "feature_gap", "low"),
    ("API rate limit too restrictive", "performance", "medium"),
]

FEATURE_TITLES = [
    "Salesforce CRM Integration", "Bulk CSV Import", "Custom Role Permissions",
    "Dark Mode UI", "Slack Notifications", "Advanced Filtering on Reports",
    "Multi-currency Billing Support", "SAML SSO Support", "Webhook Support for Events",
    "Scheduled Report Emails",
]

THEMES = ["pricing_concern", "onboarding_friction", "integration_request",
          "performance_issue", "ui_feedback", "billing_issue", "feature_gap"]

AI_INSIGHT_SAMPLES = [
    "Three accounts show declining usage_score combined with rising ticket volume in the last 14 days, suggesting onboarding gaps rather than product dissatisfaction.",
    "Feature requests tagged 'integration_request' have grown 40% quarter-over-quarter and correlate with accounts on the Growth plan, indicating a prioritization opportunity.",
    "Accounts with sentiment_score below -0.3 in the last 30 days show 3x higher churn probability based on historical patterns in this dataset.",
    "Ticket resolution time for 'critical' priority has increased, which may explain the recent dip in ticket_score across enterprise accounts.",
]


class Command(BaseCommand):
    help = "Seeds the database with realistic demo data across all CustomerOS AI models"

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing seed data...")
        AIQuery.objects.all().delete()
        AIInsight.objects.all().delete()
        RoadmapItem.objects.all().delete()
        UsageEvent.objects.all().delete()
        RiskFlag.objects.all().delete()
        HealthScoreSnapshot.objects.all().delete()
        FeedbackTheme.objects.all().delete()
        Feedback.objects.all().delete()
        Ticket.objects.all().delete()
        Feature.objects.all().delete()
        CustomerAccount.objects.all().delete()
        BusinessMetricSnapshot.objects.all().delete()
        IntegrationConfig.objects.all().delete()
        self.stdout.write("Cleared.")

        # Organization + internal users
        org, _ = Organization.objects.get_or_create(
            name="Acme SaaS Inc", defaults={"plan": "enterprise", "industry": "B2B SaaS"}
        )

        pm_user, _ = User.objects.get_or_create(
            username="priya_pm", defaults={"email": "priya@acme.com", "role": "pm", "organization": org}
        )
        analyst_user, _ = User.objects.get_or_create(
            username="arjun_analyst", defaults={"email": "arjun@acme.com", "role": "analyst", "organization": org}
        )
        cs_user, _ = User.objects.get_or_create(
            username="sarah_cs", defaults={"email": "sarah@acme.com", "role": "cs_lead", "organization": org}
        )
        for u in [pm_user, analyst_user, cs_user]:
            u.set_password("demo1234")
            u.save()

        internal_users = [pm_user, analyst_user, cs_user]

        # Customer Accounts
        accounts = []
        for name in COMPANY_NAMES:
            acc, _ = CustomerAccount.objects.get_or_create(
                organization=org,
                name=name,
                defaults={
                    "industry": random.choice(["Fintech", "Healthcare", "Retail", "Logistics", "Media"]),
                    "plan_tier": random.choice(["starter", "growth", "enterprise"]),
                    "mrr": random.randint(500, 15000),
                    "contract_start_date": timezone.now().date() - timedelta(days=random.randint(30, 700)),
                    "contract_renewal_date": timezone.now().date() + timedelta(days=random.randint(10, 365)),
                    "is_active": True,
                }
            )
            accounts.append(acc)
        self.stdout.write(f"Created {len(accounts)} customer accounts")

        # Features (created before tickets, since tickets can link to them)
        features = []
        for title in FEATURE_TITLES:
            feat, _ = Feature.objects.get_or_create(
                title=title,
                defaults={
                    "organization_account": random.choice(accounts),
                    "requested_by": random.choice(internal_users),
                    "description": f"Customer-requested capability: {title}.",
                    "status": random.choice(['proposed', 'under_review', 'planned', 'in_progress', 'shipped']),
                    "vote_count": random.randint(1, 45),
                }
            )
            features.append(feat)
        self.stdout.write(f"Created {len(features)} features")

        # Feedback + Themes
        feedback_count = 0
        for acc in accounts:
            for _ in range(random.randint(3, 5)):
                fb = Feedback.objects.create(
                    customer_account=acc,
                    submitted_by=random.choice(internal_users),
                    content=random.choice(FEEDBACK_SAMPLES),
                    source=random.choice(['survey', 'support_ticket', 'sales_call', 'email', 'nps']),
                    status=random.choice(['new', 'reviewed', 'linked']),
                    sentiment_score=round(random.uniform(-1, 1), 2),
                    urgency_score=round(random.uniform(0, 1), 2),
                )
                FeedbackTheme.objects.create(
                    feedback=fb,
                    theme_name=random.choice(THEMES),
                    confidence_score=round(random.uniform(0.6, 0.98), 2),
                )
                feedback_count += 1
        self.stdout.write(f"Created {feedback_count} feedback items")

        # Tickets
        ticket_count = 0
        for acc in accounts:
            for _ in range(random.randint(2, 4)):
                subject, category, priority = random.choice(TICKET_SUBJECTS)
                created_offset = random.randint(1, 60)
                is_resolved = random.choice([True, True, False])
                ticket = Ticket.objects.create(
                    customer_account=acc,
                    assigned_to=random.choice(internal_users),
                    subject=subject,
                    description=f"Customer reported: {subject}",
                    priority=priority,
                    category=category,
                    status='resolved' if is_resolved else random.choice(['open', 'in_progress', 'escalated']),
                    linked_feature=random.choice(features) if random.random() > 0.7 else None,
                )
                if is_resolved:
                    ticket.resolved_at = ticket.created_at + timedelta(hours=random.randint(1, 96))
                    ticket.save()
                ticket_count += 1
        self.stdout.write(f"Created {ticket_count} tickets")

        # Health Snapshots + Risk Flags
        snapshot_count = 0
        flag_count = 0
        for acc in accounts:
            usage = round(random.uniform(20, 100), 1)
            ticket_s = round(random.uniform(20, 100), 1)
            sentiment = round(random.uniform(20, 100), 1)
            adoption = round(random.uniform(20, 100), 1)
            payment = round(random.uniform(60, 100), 1)
            composite = round((usage + ticket_s + sentiment + adoption + payment) / 5, 1)

            if composite < 40:
                tier = 'critical'
            elif composite < 55:
                tier = 'at_risk'
            elif composite < 75:
                tier = 'moderate'
            else:
                tier = 'healthy'

            snapshot = HealthScoreSnapshot.objects.create(
                customer_account=acc,
                composite_score=composite,
                usage_score=usage,
                ticket_score=ticket_s,
                sentiment_score=sentiment,
                adoption_score=adoption,
                payment_score=payment,
                risk_tier=tier,
                calculation_method='rule_based',
            )
            snapshot_count += 1

            if tier in ['at_risk', 'critical']:
                RiskFlag.objects.create(
                    customer_account=acc,
                    triggering_snapshot=snapshot,
                    status=random.choice(['open', 'investigating', 'intervention_logged']),
                    trigger_reason=f"composite_score ({composite}) below healthy threshold",
                    assigned_to=cs_user,
                    intervention_notes="Scheduled a check-in call to review usage blockers." if random.random() > 0.5 else "",
                )
                flag_count += 1
        self.stdout.write(f"Created {snapshot_count} health snapshots, {flag_count} risk flags")

        # Usage Events
        event_names = ['dashboard_viewed', 'feature_request_created', 'ai_insight_viewed',
                       'ticket_viewed', 'account_health_viewed', 'roadmap_viewed']
        event_count = 0
        for acc in accounts:
            for _ in range(random.randint(8, 15)):
                UsageEvent.objects.create(
                    customer_account=acc,
                    user=random.choice(internal_users),
                    event_name=random.choice(event_names),
                    properties={"sample": True},
                    source='internal',
                )
                event_count += 1
        self.stdout.write(f"Created {event_count} usage events")

        # Roadmap Items
        roadmap_count = 0
        for feat in random.sample(features, k=min(6, len(features))):
            item = RoadmapItem.objects.create(
                title=feat.title,
                description=feat.description,
                status=random.choice(['backlog', 'planned', 'in_progress', 'shipped']),
                priority_score=round(random.uniform(40, 95), 1),
                target_quarter=random.choice(['Q1', 'Q2', 'Q3', 'Q4']),
                target_year=2026,
                owner=pm_user,
            )
            item.linked_features.add(feat)
            roadmap_count += 1
        self.stdout.write(f"Created {roadmap_count} roadmap items")

        # AI Insights + Queries (tagged as seed data, not real model output)
        insight_count = 0
        for text in AI_INSIGHT_SAMPLES:
            for _ in range(3):
                AIInsight.objects.create(
                    insight_type=random.choice(['feedback_theme', 'churn_risk', 'prioritization', 'copilot_answer']),
                    status=random.choice(['generated', 'viewed', 'accepted', 'rejected']),
                    customer_account=random.choice(accounts),
                    generated_for_user=pm_user,
                    prompt_input="Why are these accounts at risk?",
                    response_text=text,
                    model_used='seed_demo_data',  # tagged so it's excludable later
                    latency_ms=random.randint(300, 2200),
                )
                insight_count += 1
        self.stdout.write(f"Created {insight_count} AI insights (tagged seed_demo_data)")

        AIQuery.objects.create(
            asked_by=pm_user,
            query_text="Why are these accounts at risk?",
        )
        AIQuery.objects.create(
            asked_by=pm_user,
            query_text="Which features drive the most retention?",
        )

        # Integration Configs
        IntegrationConfig.objects.get_or_create(
            organization=org, provider='jira',
            defaults={"config": {"project_key": "COS"}, "is_active": True}
        )
        IntegrationConfig.objects.get_or_create(
            organization=org, provider='mixpanel',
            defaults={"config": {"project_id": "demo"}, "is_active": True}
        )

        # Business Metric Snapshots
        for metric_name, value in [
            ("decision_velocity_weekly", 6),
            ("ai_acceptance_rate", 0.62),
            ("feature_conversion_rate", 0.18),
            ("avg_time_to_risk_detection_days", 4.2),
        ]:
            BusinessMetricSnapshot.objects.create(metric_name=metric_name, metric_value=value)

        self.stdout.write(self.style.SUCCESS("Seed complete."))