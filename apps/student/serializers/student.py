from django.db import transaction

from rest_framework import serializers

from apps.student import models
from apps.account.models import Employee
from apps.account.employee.serializers import EmployeeListSerializer


class StudentListSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField(method_name='get_payment')
    employee = EmployeeListSerializer(read_only=True)

    class Meta:
        model = models.Student
        fields = [
            'id', 'student_id_time', 'full_name', 'phone_number', 'tariff', 'course_price', 'paid', 'debt', 'group_joined', 'status', 'payment', 'employee', 'student_id', 'contract_number', 'suprice', 'telegram_id'
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
    group = serializers.SerializerMethodField(method_name='get_student_group')

    class Meta:
        model = models.Student
        fields = [
            'id', 'full_name', 'phone_number', 'contract_number', 'course_price', 'paid', 'group_joined', 'debt', 'tariff', 'employee', 'suprice', 'student_id', 'student_id_time', 'month', 'suprice', 'telegram_id', 'telegram_full_name', 'telegram_username', 'type', 'is_blacklist', 'group'
        ]
        
    def get_student_group(self, obj):
        group = models.StudentGroup.objects.filter(students=obj).last()
        return {
            'id': group.id if group else None,
            'name': group.group_name if group else None
        }


class StudentUpdateSerializer(serializers.ModelSerializer):
    group = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Student
        fields = [
            'full_name', 'phone_number', 'contract_number', 'course_price', 'paid',
            'group_joined', 'debt', 'tariff', 'employee', 'suprice', 'student_id',
            'student_id_time', 'month', 'type', 'is_blacklist', 'group'
        ]

    def validate_group(self, value):
        if not models.StudentGroup.objects.filter(id=value).exists():
            raise serializers.ValidationError("Group not found")
        return value
    
    def update(self, instance, validated_data):
        fields = [
            'full_name', 'phone_number', 'contract_number', 'course_price', 'paid',
            'group_joined', 'debt', 'tariff', 'employee', 'suprice', 'student_id',
            'student_id_time', 'month', 'type', 'is_blacklist'
        ]
        for field in fields:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        group = models.StudentGroup.objects.get(id=validated_data.get('group'))
        group.students.add(instance)
        group.save()
        instance.save()
        return instance 


class StudentServiceAddSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    contract_number = serializers.CharField()
    tariff = serializers.ChoiceField(choices=models.Student.TARIFF)
    employee_id = serializers.IntegerField()
    coach_id = serializers.IntegerField()

    def validate(self, data):
        employee = Employee.objects.filter(id=data['employee_id']).first()
        coach = Employee.objects.filter(id=data['coach_id']).first()
        if not employee:
            raise serializers.ValidationError("Employee not found")
        if not coach:
            raise serializers.ValidationError("Coach not found")
        data['employee'] = employee
        data['coach'] = coach
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            return models.Student.objects.create(
                full_name=validated_data.get('full_name'),
                phone_number=validated_data.get('phone_number'),
                contract_number=validated_data.get('contract_number'),
                tariff=validated_data.get('tariff'),
                employee=validated_data.get('employee'),
                coach=validated_data.get('coach'),
            )