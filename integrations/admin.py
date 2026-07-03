from django.contrib import admin
from .models import IntegrationConfig


@admin.register(IntegrationConfig)
class IntegrationConfigAdmin(admin.ModelAdmin):
    list_display = ('organization', 'provider', 'is_active', 'last_synced_at')
    list_filter = ('provider', 'is_active')