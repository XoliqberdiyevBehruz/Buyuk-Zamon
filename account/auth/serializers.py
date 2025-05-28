from django.db import transaction
from django.contrib.auth.hashers import check_password

from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken

from account import models 


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        try:
            user = models.User.objects.get(phone_number=phone_number)
        except models.User.DoesNotExist:
            raise serializers.ValidationError('Invalid phone number or password')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid phone number or password')

        if not user.is_active:
            raise serializers.ValidationError('User is inactive')

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': user.role
        }