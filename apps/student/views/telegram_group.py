from django.shortcuts import get_object_or_404

from rest_framework import views
from rest_framework.response import Response

from apps.student.serializers.telegram_group import StudentTelegramGroupsSerializer
from apps.student import models
from apps.account import permissions

class StudentTelegramGroupListSerializer(views.APIView):
    permission_classes = [permissions.IsBossOrEmployee]

    def get(self, request, id):
        student = get_object_or_404(models.Student, id=id)
        telegram_groups = models.TelegramGroup.objects.filter(students=student)
        serializer = StudentTelegramGroupsSerializer(telegram_groups, many=True)
        return Response(serializer.data, status=200)