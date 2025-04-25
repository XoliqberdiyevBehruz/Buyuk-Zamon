from django.db import transaction

from rest_framework import serializers

from account import models 


class StudentCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    father_name = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    phone_number = serializers.CharField()
    passwort_series = serializers.CharField(required=False)
    birth_place = serializers.CharField(required=False)
    live_place = serializers.CharField(required=False)
    profile_photo = serializers.ImageField(required=False)

    def validate_phone_number(self, phone_number):
        
        if models.Student.objects.filter(phone_number=phone_number).first():
            raise serializers.ValidationError("this phone number already taken")
        
        return phone_number 


    def validate_passport_series(self, passport_series):
        if passport_series and models.Student.objects.filter(passport_series=passport_series).first():
                raise serializers.ValidationError("this passport_series already taken")
        return passport_series 


    def create(self, validated_data):
        with transaction.atomic():
            student = models.Student.objects.create(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                father_name=validated_data.get('father_name', None),
                birth_date=validated_data.get('birth_date', None),
                phone_number=validated_data['phone_number'],
                passport_series=validated_data.get('passport_series', None),
                birth_place=validated_data.get('birth_place', None),
                live_address=validated_data.get('live_place', None),
                profile_photo=validated_data.get('profile_photo', None)
            )
            return student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = [
            'id', 'first_name', 'last_name', 'father_name', 'birth_date', 'phone_number',
            'passport_series', 'birth_place', 'live_address', 'profile_photo'
        ]


class StudentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = [
            'id', 'first_name', 'last_name', 'phone_number', 'profile_photo'
        ]