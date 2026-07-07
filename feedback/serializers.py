from rest_framework import serializers
from .models import Feedback, FeedbackTheme


class FeedbackThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackTheme
        fields = ['id', 'theme_name', 'confidence_score']


class FeedbackSerializer(serializers.ModelSerializer):
    themes = FeedbackThemeSerializer(many=True, read_only=True)
    customer_account_name = serializers.CharField(
        source='customer_account.name', read_only=True
    )

    class Meta:
        model = Feedback
        fields = [
            'id', 'customer_account', 'customer_account_name',
            'content', 'source', 'status',
            'sentiment_score', 'urgency_score',
            'themes', 'created_at'
        ]