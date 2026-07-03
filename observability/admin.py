from django.contrib import admin
from .models import BusinessMetricSnapshot


@admin.register(BusinessMetricSnapshot)
class BusinessMetricSnapshotAdmin(admin.ModelAdmin):
    list_display = ('metric_name', 'metric_value', 'created_at')
    list_filter = ('metric_name',)