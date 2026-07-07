from rest_framework import serializers
from .models import HealthScoreSnapshot, RiskFlag


class HealthScoreSnapshotSerializer(serializers.ModelSerializer):
    customer_account_name = serializers.CharField(
        source='customer_account.name', read_only=True
    )

    class Meta:
        model = HealthScoreSnapshot
        fields = [
            'id', 'customer_account', 'customer_account_name',
            'composite_score', 'usage_score', 'ticket_score',
            'sentiment_score', 'adoption_score', 'payment_score',
            'risk_tier', 'calculation_method', 'created_at'
        ]


class RiskFlagSerializer(serializers.ModelSerializer):
    customer_account_name = serializers.CharField(
        source='customer_account.name', read_only=True
    )
    days_open = serializers.IntegerField(read_only=True)

    class Meta:
        model = RiskFlag
        fields = [
            'id', 'customer_account', 'customer_account_name',
            'status', 'trigger_reason', 'intervention_notes',
            'days_open', 'resolved_at', 'created_at'
        ]


class AIInsightSerializer(serializers.ModelSerializer):
    class Meta:
        from ai_engine.models import AIInsight
        model = AIInsight
        fields = [
            'id', 'insight_type', 'status', 'customer_account',
            'response_text', 'model_used', 'latency_ms',
            'rejection_reason', 'created_at'
        ]