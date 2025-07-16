from django.db import transaction

from rest_framework import serializers

from student import models
from account.models import Employee
from account.employee.serializers import EmployeeListSerializer


class StudentListSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField(method_name='get_payment')
    employee = EmployeeListSerializer(read_only=True)

    class Meta:
        model = models.Student
        fields = [
            'id', 'student_id_time', 'full_name', 'phone_number', 'tariff', 'course_price', 'paid', 'debt',   
            'group_joined', 'status', 'payment', 'employee', 'student_id', 'contract_number', 'suprice', 'telegram_id'
        ]

    def get_payment(self, obj):
        payment = models.Payment.objects.filter(user=obj).order_by('-created_at').first()
        if payment:
            return {
                "payment_time": payment.payment_time,
                "payment_type": payment.type,
                "payment_bank": payment.bank
            }
        return None


class StudentAddSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = models.Student
        fields = [
            'full_name', 'phone_number', 'contract_number', 'tariff', 'course_price', 'student_id_time', 'employee', 'student_id', 'month'
        ]

    def create(self, validated_data):
        with transaction.atomic():
            student = models.Student.objects.create(
                full_name=validated_data['full_name'],
                phone_number=validated_data['phone_number'],
                contract_number=validated_data.get('contract_number', None),
                tariff=validated_data['tariff'],
                course_price=validated_data.get('course_price', None),
                debt=validated_data.get('course_price', None),
                is_debt=True,
                paid=0,
                student_id_time=validated_data.get('student_id_time', None),
                employee=validated_data.get('employee'),
                student_id=validated_data.get('student_id'),
                month=validated_data.get('month'),
            )
            return student
        
    
class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = [
            'id', 'full_name', 'phone_number', 'contract_number', 'course_price', 'paid', 'group_joined', 'debt', 'tariff', 'employee', 'suprice', 'student_id', 'student_id_time', 'month', 'suprice', 'telegram_id', 'telegram_full_name', 'telegram_username',
            'type', 'is_blacklist'
        ]


class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = [
            'id', 'full_name', 'phone_number', 'contract_number', 'description'
        ]

    
class StudentSendMessageSerializer(serializers.Serializer):
    ids = serializers.ListSerializer(child=serializers.CharField())
    message = serializers.CharField()


class GroupCreateSerializer(serializers.Serializer):
    group_name = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    start_date_online = serializers.DateField()
    start_date_offline = serializers.DateField()

    def create(self, validated_data):
        with transaction.atomic():
            group = models.StudentGroup.objects.create(
                group_name=validated_data.get('group_name'),
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date'),
                start_date_online=validated_data.get('start_date_online'),
                start_date_offline=validated_data.get("start_date_offline"),
            )
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

    
class StudentTelegramGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TelegramGroup
        fields = [
            'id', 'name'
        ]