from rest_framework import serializers
from .models import AIInsight, AIQuery


class AIInsightSerializer(serializers.ModelSerializer):
    customer_account_name = serializers.SerializerMethodField()

    class Meta:
        model = AIInsight
        fields = [
            'id', 'insight_type', 'status',
            'customer_account', 'customer_account_name',
            'response_text', 'model_used', 'latency_ms',
            'rejection_reason', 'created_at'
        ]

    def get_customer_account_name(self, obj):
        if obj.customer_account:
            return obj.customer_account.name
        return None


class AIQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AIQuery
        fields = ['id', 'query_text', 'created_at']