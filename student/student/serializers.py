from django.db import transaction

from rest_framework import serializers

from student import models
from account.models import Employee


class StudentListSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField(method_name='get_payment')

    class Meta:
        model = models.Student
        fields = [
            'id', 'student_id_time', 'full_name', 'phone_number', 'tariff', 'course_price', 'paid', 'debt',   
            'group_joined', 'status', 'payment', 
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
            'full_name', 'phone_number', 'contract_number', 'payment_type', 'tariff', 'course_price', 'student_id_time', 'employee'
        ]

    # def validate(self, data):
    #     try:
    #         employee = Employee.objects.get(id=data['employee'])
    #     except Employee.DoesNotExist:
    #         raise serializers.ValidationError("Employee does not exist.")
    #     data['employee'] = employee
    #     return data

    def create(self, validated_data):
        with transaction.atomic():
            student = models.Student.objects.create(
                full_name=validated_data['full_name'],
                phone_number=validated_data['phone_number'],
                contract_number=validated_data.get('contract_number', None),
                payment_type=validated_data['payment_type'],
                tariff=validated_data['tariff'],
                course_price=validated_data.get('course_price', None),
                debt=validated_data.get('debt', None),
                is_debt=True,
                paid=0,
                student_id_time=validated_data.get('student_id_time', None),
                employee=validated_data.get('employee')
            )
            return student
        
    
class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = [
            'id', 'full_name', 'phone_number', 'contract_number', 'course_price', 'paid', 'group_joined', 'debt', 'tariff'
        ]