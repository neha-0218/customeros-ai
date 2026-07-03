from django.contrib import admin
from .models import Feature


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization_account', 'status', 'vote_count', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')