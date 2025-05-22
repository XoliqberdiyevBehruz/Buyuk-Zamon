from django.db import transaction  
from django.db.models import Sum
from django.utils import timezone

from rest_framework import serializers

from account import models 
from finance.models import Expence, ExpenceCategory


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = ['id', 'name', ]


class EmployeeCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    position_id = serializers.IntegerField()
    date_of_joined = serializers.DateField()

    def validate(self, data):
        try:
            postion = models.Position.objects.get(id=data['position_id'])
        except models.Position.DoesNotExist:
            raise serializers.ValidationError("Position does not exist")
        data['position'] = postion
        return data 
    
    def create(self, validated_data):
        with transaction.atomic():
            employee = models.Employee.objects.create(
                full_name=validated_data['full_name'],
                phone_number=validated_data['phone_number'],
                position=validated_data['position'],
                date_of_joined=validated_data.get('date_of_joined')
            )
            return employee
        return None
    

class EmployeeListSerializer(serializers.ModelSerializer):
    position = PositionSerializer()
    paid = serializers.SerializerMethodField(method_name='get_employee_salary')

    class Meta:
        model = models.Employee
        fields = ['id', 'full_name', 'phone_number', 'position', 'paid', 'date_of_joined']

    def get_employee_salary(self, obj):
        employee_salary = models.EmployeeSalary.objects.filter(employee=obj, date__month=timezone.now().month)
        return employee_salary.aggregate(paid=Sum('salary'))['paid'] if employee_salary.aggregate(paid=Sum('salary'))['paid'] else 0


class EmployeeDetailSerializer(serializers.ModelSerializer):
    position = PositionSerializer()

    class Meta:
        model = models.Employee
        fields = ['id', 'full_name', 'phone_number', 'position', 'paid', 'date_of_joined']



class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = ['full_name', 'phone_number', 'position', 'paid', 'date_of_joined']
        extra_kwargs = {
            'full_name': {'required': False},
            'phone_number': {'required': False},
            'position': {'required': False},
            'paid': {'required': False},
            'date_of_joined': {'required': False}
        }


class EmployeeSalaryCreateSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    salary = serializers.IntegerField()
    date = serializers.DateField()

    def validate(self, data):
        try:
            employee = models.Employee.objects.get(id=data['employee_id'])
        except models.Employee.DoesNotExist:
            raise serializers.ValidationError("Employee does not exist")
        data['employee'] = employee
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            salary = models.EmployeeSalary.objects.create(
                employee=validated_data['employee'],
                salary=validated_data['salary'],
                date=validated_data['date']
            )       
            return salary
        return None
    

class EmployeeDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = [
            'id', 'full_name', 'paid'
        ]

    