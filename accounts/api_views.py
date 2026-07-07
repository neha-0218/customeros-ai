from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomerAccount
from .serializers import CustomerAccountSerializer


class CustomerAccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API for customer accounts.
    Scoped to the authenticated user's organization.
    Supports filtering by plan_tier and is_active.
    Supports ordering by mrr, name, created_at.
    """
    serializer_class = CustomerAccountSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['plan_tier', 'is_active']
    search_fields = ['name', 'industry']
    ordering_fields = ['mrr', 'name', 'created_at']
    ordering = ['-mrr']

    def get_queryset(self):
        return CustomerAccount.objects.filter(
            organization=self.request.user.organization,
            is_active=True
        ).prefetch_related('health_snapshots')