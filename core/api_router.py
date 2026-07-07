from rest_framework.routers import DefaultRouter
from accounts.api_views import CustomerAccountViewSet
from feedback.api_views import FeedbackViewSet
from tickets.api_views import TicketViewSet
from health.api_views import HealthScoreViewSet, RiskFlagViewSet
from ai_engine.api_views import AIInsightViewSet

router = DefaultRouter()
router.register(r'accounts', CustomerAccountViewSet, basename='api-accounts')
router.register(r'feedback', FeedbackViewSet, basename='api-feedback')
router.register(r'tickets', TicketViewSet, basename='api-tickets')
router.register(r'health', HealthScoreViewSet, basename='api-health')
router.register(r'risk-flags', RiskFlagViewSet, basename='api-risk-flags')
router.register(r'ai-insights', AIInsightViewSet, basename='api-ai-insights')