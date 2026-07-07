from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import HealthScoreSnapshot, RiskFlag
from .serializers import HealthScoreSnapshotSerializer, RiskFlagSerializer


class HealthScoreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HealthScoreSnapshotSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['risk_tier']
    ordering_fields = ['composite_score', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return HealthScoreSnapshot.objects.filter(
            customer_account__organization=self.request.user.organization
        ).select_related('customer_account')


class RiskFlagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RiskFlagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering = ['-created_at']

    def get_queryset(self):
        return RiskFlag.objects.filter(
            customer_account__organization=self.request.user.organization
        ).select_related('customer_account')