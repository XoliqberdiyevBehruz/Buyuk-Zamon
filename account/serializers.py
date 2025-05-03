from django.utils import timezone
from django.db import transaction
from django.db.models import Sum

from rest_framework import serializers

from account import models, utils

class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = [
            'full_name', 'phone_number', 'card_number', 'group_id',
        ]
        extra_kwargs = (
            {"full_name": {'required': False}, "phone_number": {'required': False}, 'card_number': {'required': False}, 'group_id': {'required': False}}
        )

    def create(self, validated_date):
        with transaction.atomic():
            student = models.Student.objects.create(
                full_name=validated_date['full_name'],
                phone_number=validated_date['phone_number'],
                card_number=validated_date['card_number'],
                group_id=validated_date['group_id'],
                is_debt=True
            )
            return student


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            'user', 'payment_time', 'price', 'payment_id'
        ]

        extra_kwargs = (
            {"user": {'required': False}, "payment_time": {'required': False}, 'price': {'required': False}, 'payment_id': {'required': False}}
        )
    
    def create(self, validated_data):
        with transaction.atomic():
            return models.Payment.objects.create(**validated_data)


class PaymentGetSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    payment_id = serializers.CharField()


class UserGetSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    card_number = serializers.CharField(required=False)


class AddTotalPriceSerializer(serializers.Serializer):
    total_price = serializers.CharField()



class StudentListSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField(method_name='get_payment')

    class Meta:
        model = models.Student
        fields = [
            'id', 'full_name', 'phone_number', 'contract_number', 'course_price', 'paid', 'debt', 'is_debt', 'tariff',  
            'payment', 'group_joined'
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
    class Meta:
        model = models.Student
        fields = [
            'full_name', 'phone_number', 'contract_number', 'payment_type', 'tariff'
        ]
    
    def create(self, validated_data):
        with transaction.atomic():
            course_price = utils.get_course_price(validated_data['payment_type'], validated_data['tariff'])
            student = models.Student.objects.create(
                full_name=validated_data['full_name'],
                phone_number=validated_data['phone_number'],
                contract_number=validated_data.get('contract_number', None),
                payment_type=validated_data['payment_type'],
                tariff=validated_data['tariff'],
                course_price=course_price,
                debt=course_price,
                is_debt=True,
                paid=0,
            )
            return student
        
    
class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = [
            'id', 'full_name', 'phone_number', 'contract_number', 'course_price', 'paid', 'group_joined', 'debt', 'tariff'
        ]


class PaymentAddSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    price = serializers.IntegerField()

    def validate(self, data):
        try:
            student = models.Student.objects.get(id=data['user_id'])
        except models.Student.DoesNotExist:
            raise serializers.ValidationError('student not found')  
        data['student'] = student
        return data

    def create(self, validated_data):
        with transaction.atomic():
            payment = models.Payment.objects.create(
                user=validated_data['student'],
                price=validated_data['price'],
                payment_time=timezone.now(),
                type='naqd'
            )    
            return payment
        
    
class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            'id', 'payment_time', 'price', 'type'
        ]
    

class PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            'price'
        ]

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance