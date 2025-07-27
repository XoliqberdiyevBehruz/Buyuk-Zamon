from django.db import transaction

from rest_framework import serializers

from apps.student import models


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
    

class StudentDescriptionSerializer(serializers.Serializer):
    description = serializers.CharField()
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    contract_number = serializers.CharField()

    def create(self, validated_data):
        with transaction.atomic():
            student_description = models.Notification.objects.create(
                description=validated_data.get('description'),
                full_name=validated_data.get('full_name'),
                phone_number=validated_data.get('phone_number'),
                contract_number=validated_data.get('contract_number'),
            )
            return student_description
        return None


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = [
            'telegram_id', 'telegram_full_name', 'telegram_username'
        ]

    def update(self, instance, validated_data):
        instance.telegram_id = validated_data.get('telegram_id')
        instance.telegram_full_name = validated_data.get('telegram_full_name')
        instance.telegram_username = validated_data.get('telegram_username')
        instance.save()
        return instance
    

class TelegramGroupCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    group_id = serializers.IntegerField()
    type = serializers.CharField()

    def create(self, validated_data):
        with transaction.atomic():
            telegram_group = models.TelegramGroup.objects.create(**validated_data)
            return telegram_group
    

class TelegramGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TelegramGroup
        fields = ['id', 'name', 'group_id']

    
class StudentSetTelegramGroupSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()

    def validate(self, attrs):
        try:
            student = models.Student.objects.get(id=attrs.get('student_id'))
        except models.TelegramGroup.DoesNotExist:
            raise serializers.ValidationError("not found")
        attrs['student'] = student
        return attrs

    def update(self, instance, validated_data):
        instance.students.set([validated_data.get('student')])
        instance.save()
        return instance


class StudentGroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentGroup
        fields = [
            'id', 'group_name'
        ]


class StudentMessageCreateSerializer(serializers.Serializer):
    message = serializers.CharField()
    telegram_id = serializers.CharField()

    def validate(self, data):
        try:
            student = models.Student.objects.get(telegram_id=data.get('telegram_id'))
        except models.Student.DoesNotExist:
            raise serializers.ValidationError({'detail': "Student not found"})
        data['student'] = student
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            message = models.StudentMessage.objects.create(
                message=validated_data.get('message'),
                student=validated_data.get('student')
            )
            return message