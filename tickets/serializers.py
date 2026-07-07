from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    customer_account_name = serializers.CharField(
        source='customer_account.name', read_only=True
    )
    resolution_time_hours = serializers.FloatField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'customer_account', 'customer_account_name',
            'subject', 'description', 'priority', 'category',
            'status', 'linked_feature', 'resolved_at',
            'resolution_time_hours', 'created_at'
        ]