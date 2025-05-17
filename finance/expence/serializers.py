from django.db import transaction 

from rest_framework import serializers

from finance import models


class ExpenceCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExpenceCategory
        fields = [
            'id', 'name'
        ]


class ExpenceAddSerializer(serializers.Serializer):
    name = serializers.CharField()
    category_id = serializers.IntegerField()
    date = serializers.DateField()
    price = serializers.IntegerField()
    description = serializers.CharField()

    def validate(self, data):
        try:
            category = models.ExpenceCategory.objects.get(id=data.get('category_id'))
        except models.ExpenceCategory.DoesNotExist:
            raise serializers.ValidationError("category not found")
        return data

    def create(self, validated_data):
        with transaction.atomic():
            return models.Expence.objects.create(
                **validated_data
            )
        return None


class ExpenceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expence
        fields = [
            'id', 'name', 'date', 'price', 'description'
        ]
    

class ExpenceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expence
        fields = [
            'name', 'date', 'price', 'description'
        ]

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.date = validated_data.get('date', instance.date)
            instance.price = validated_data.get('price', instance.price)
            instance.description = validated_data.get('description', instance.description)
            instance.save()
            return instance 
        return None