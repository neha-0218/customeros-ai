from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import AIInsight
from .serializers import AIInsightSerializer


class AIInsightViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AIInsightSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['insight_type', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        return AIInsight.objects.filter(
            generated_for_user__organization=self.request.user.organization
        ).exclude(model_used='seed_demo_data')