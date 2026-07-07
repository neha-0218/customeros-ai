from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['source', 'status']
    search_fields = ['content']
    ordering_fields = ['sentiment_score', 'urgency_score', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Feedback.objects.filter(
            customer_account__organization=self.request.user.organization
        ).select_related('customer_account').prefetch_related('themes')