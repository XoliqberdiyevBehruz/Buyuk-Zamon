from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response


from apps.student.serializers import student_message as student_message_serializer
from apps.student import models, tasks
from apps.account import permissions


class StudentMessageListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsBossOrEmployee]
    queryset = models.StudentMessage.objects.select_related('student')
    serializer_class = student_message_serializer.StudentMessageListSerializer


class StudentSendMessageApiView(generics.GenericAPIView):
    serializer_class = student_message_serializer.StudentSendMessageSerializer
    queryset = models.Student.objects.all()
    permission_classes = [permissions.IsBossOrEmployee]

    def post(self, request):
        serializer = student_message_serializer.StudentSendMessageSerializer(data=request.data)
        if serializer.is_valid():
            for id in serializer.data.get('ids'):
                tasks.send_telegram_message.delay(settings.BOT_TOKEN, id, serializer.data.get('message'))
            return Response({"message": "send"}, status=status.HTTP_200_OK)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    
