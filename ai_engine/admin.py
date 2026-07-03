from django.contrib import admin
from .models import AIInsight, AIQuery


@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    list_display = ('insight_type', 'status', 'customer_account', 'model_used', 'latency_ms', 'created_at')
    list_filter = ('insight_type', 'status', 'model_used')


@admin.register(AIQuery)
class AIQueryAdmin(admin.ModelAdmin):
    list_display = ('query_text', 'asked_by', 'created_at')