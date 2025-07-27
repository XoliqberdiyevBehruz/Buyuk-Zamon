from rest_framework import generics

from apps.student.serializers import notification as notification_serializer
from apps.student import models
from apps.account import permissions


class NotificationListApiView(generics.ListAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = notification_serializer.NotificationListSerializer
    permission_classes = [permissions.IsBossOrEmployee]
