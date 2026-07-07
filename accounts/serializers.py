from rest_framework import serializers
from .models import Organization, CustomerAccount, User


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'plan', 'industry', 'created_at']


class CustomerAccountSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(
        source='organization.name', read_only=True
    )
    health_score = serializers.SerializerMethodField()

    class Meta:
        model = CustomerAccount
        fields = [
            'id', 'name', 'industry', 'plan_tier', 'mrr',
            'contract_renewal_date', 'is_active',
            'organization_name', 'health_score', 'created_at'
        ]

    def get_health_score(self, obj):
        latest = obj.health_snapshots.order_by('-created_at').first()
        if latest:
            return {
                'composite_score': latest.composite_score,
                'risk_tier': latest.risk_tier,
            }
        return None