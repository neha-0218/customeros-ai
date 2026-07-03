from django.contrib import admin
from .models import RoadmapItem


@admin.register(RoadmapItem)
class RoadmapItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority_score', 'target_quarter', 'target_year', 'owner')
    list_filter = ('status', 'target_quarter')