
from rest_framework import serializers

from apps.student import models


class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = [
            'id', 'full_name', 'phone_number', 'contract_number', 'description'
        ]