from django.db import transaction

from rest_framework import serializers

from apps.student import models


class PaymentAddSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    price = serializers.IntegerField()
    payment_time = serializers.DateField()
    type = serializers.ChoiceField(choices=models.Payment.PAYMENT_TYPE)
    bank = serializers.ChoiceField(choices=models.Payment.BANK, required=False)

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
                payment_time=validated_data['payment_time'],
                type=validated_data['type'],
                bank=validated_data.get('bank', None),
            )   
            return payment


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            'id', 'payment_time', 'price', 'type', 'bank'
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


class PaymentImagesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentImage
        fields = [
            'payment', 'image'
        ]
    
    def create(self, validated_data):
        with transaction.atomic():
            return models.PaymentImage.objects.create(**validated_data)