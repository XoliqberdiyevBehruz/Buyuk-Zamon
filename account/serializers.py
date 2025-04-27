from django.db import transaction

from rest_framework import serializers

from account import models 

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
    class Meta:
        model = models.Student
        fields = [
            'id', 'full_name', 'phone_number', 'contract_number', 'course_price', 'paid', 'debt', 'is_debt'
        ]


class StudentAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = [
            'full_name', 'phone_number', 'telegram_link', 'contract_number', 'course_price'
        ]
    
    def create(self, validated_data):
        with transaction.atomic():
            student = models.Student.objects.create(
                full_name=validated_data['full_name'],
                phone_number=validated_data['phone_number'],
                telegram_link=validated_data['telegram_link'],
                contract_number=validated_data['contract_number'],
                course_price=validated_data['course_price'],
                debt=validated_data['course_price'],
                is_debt=True,
            )
            return student