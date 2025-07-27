from rest_framework import serializers

from apps.student.serializers.student import StudentListSerializer

from apps.student import models


class StudentSendMessageSerializer(serializers.Serializer):
    ids = serializers.ListSerializer(child=serializers.CharField())
    message = serializers.CharField()


class StudentMessageListSerializer(serializers.ModelSerializer):
    student = StudentListSerializer()
    
    class Meta:
        model = models.StudentMessage
        fields = ['id', 'message', 'student']