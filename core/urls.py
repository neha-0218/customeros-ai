from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.api_router import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/feedback/', include('feedback.urls')),
    path('api/tickets/', include('tickets.urls')),
    path('api/features/', include('features.urls')),
    path('api/health/', include('health.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/roadmap/', include('roadmap.urls')),
    path('api/ai/', include('ai_engine.urls')),
    path('api/integrations/', include('integrations.urls')),
    path('api/observability/', include('observability.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/v1/', include(router.urls)),
    path('', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


