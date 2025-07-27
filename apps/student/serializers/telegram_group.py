from rest_framework import serializers

from apps.student import models


class StudentTelegramGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TelegramGroup
        fields = [
            'id', 'name'
        ]