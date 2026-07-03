from django.contrib import admin
from .models import HealthScoreSnapshot, RiskFlag


@admin.register(HealthScoreSnapshot)
class HealthScoreSnapshotAdmin(admin.ModelAdmin):
    list_display = ('customer_account', 'composite_score', 'risk_tier', 'calculation_method', 'created_at')
    list_filter = ('risk_tier', 'calculation_method')


@admin.register(RiskFlag)
class RiskFlagAdmin(admin.ModelAdmin):
    list_display = ('customer_account', 'status', 'trigger_reason', 'assigned_to', 'created_at', 'resolved_at')
    list_filter = ('status',)