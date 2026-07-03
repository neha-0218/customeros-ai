from django.contrib import admin
from .models import Feedback, FeedbackTheme


class FeedbackThemeInline(admin.TabularInline):
    model = FeedbackTheme
    extra = 0


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('customer_account', 'source', 'status', 'sentiment_score', 'urgency_score', 'created_at')
    list_filter = ('source', 'status')
    search_fields = ('content',)
    inlines = [FeedbackThemeInline]


@admin.register(FeedbackTheme)
class FeedbackThemeAdmin(admin.ModelAdmin):
    list_display = ('theme_name', 'feedback', 'confidence_score')