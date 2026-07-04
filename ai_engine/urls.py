from django.urls import path
from . import views

urlpatterns = [
    path('insights/', views.ai_insight_list, name='ai_insight_list'),
    path('insights/<uuid:pk>/', views.ai_insight_detail, name='ai_insight_detail'),
    path('generate/churn/<uuid:account_pk>/', views.generate_churn_insight, name='generate_churn_insight'),
    path('generate/features/', views.generate_feature_insight, name='generate_feature_insight'),
    path('generate/feedback/', views.generate_feedback_insight, name='generate_feedback_insight'),
    path('copilot/', views.ai_copilot, name='ai_copilot'),
    path('copilot/ask/', views.ai_copilot_ask, name='ai_copilot_ask'),
]
