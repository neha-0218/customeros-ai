from django.contrib import admin
from .models import UsageEvent


@admin.register(UsageEvent)
class UsageEventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'customer_account', 'source', 'created_at')
    list_filter = ('event_name', 'source')