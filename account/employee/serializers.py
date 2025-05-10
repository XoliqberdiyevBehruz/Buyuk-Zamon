from django.db import transaction  

from rest_framework import serializers

from account import models 


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = ['id', 'name', ]


class EmployeeCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    position_id = serializers.IntegerField()

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
                position=validated_data['position']
            )
            return employee
        return None
    

class EmployeeListSerializer(serializers.ModelSerializer):
    position = PositionSerializer()

    class Meta:
        model = models.Employee
        fields = ['id', 'full_name', 'phone_number', 'position']


class EmployeeDetailSerializer(serializers.ModelSerializer):
    position = PositionSerializer()

    class Meta:
        model = models.Employee
        fields = ['id', 'full_name', 'phone_number', 'position']



class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = [ 'full_name', 'phone_number', 'position']
        extra_kwargs = {
            'full_name': {'required': False},
            'phone_number': {'required': False},
            'position': {'required': False},
        }

