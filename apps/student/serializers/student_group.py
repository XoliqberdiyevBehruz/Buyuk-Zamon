from django.db import transaction

from rest_framework import serializers

from apps.student import models
from apps.account.models import Employee
from apps.account.employee.serializers import EmployeeListSerializer


class GroupCreateSerializer(serializers.Serializer):
    group_name = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    start_date_online = serializers.DateField()
    start_date_offline = serializers.DateField()
    student_start_date = serializers.DateField()
    student_end_date = serializers.DateField()

    def create(self, validated_data):
        with transaction.atomic():
            group = models.StudentGroup.objects.create(
                group_name=validated_data.get('group_name'),
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date'),
                start_date_online=validated_data.get('start_date_online'),
                start_date_offline=validated_data.get("start_date_offline"),
                student_start_date=validated_data.get('student_start_date'),
                student_end_date=validated_data.get('student_end_date'),
            )
            start_datetime = validated_data.get('student_start_date')
            end_datetime = validated_data.get('student_end_date')
            students = models.Student.objects.filter(
                student_id_time__range=(start_datetime, end_datetime)
            )
            for student in students:
                student.group = group
                student.save() 
            return group
        
    
class GroupAddStudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = [
            'id', 'full_name'
        ]


class GroupStudentListSerializer(serializers.ModelSerializer):
    employee = EmployeeListSerializer(read_only=True)

    class Meta:
        model = models.Student
        fields = [
            'id', 'student_id_time', 'full_name', 'phone_number', 'tariff', 'course_price', 'paid', 'debt',   
            'group_joined', 'status', 'employee', 'student_id', 'contract_number', 'suprice', 'telegram_id'
        ]
        
    
class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentGroup
        fields = [
            'id', 'group_name'
        ]
