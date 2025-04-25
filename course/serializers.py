from django.db import transaction

from rest_framework import serializers

from course import models 
from account.serializers import StudentPaymentSerializer


class PaymentCreateSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    student_id = serializers.IntegerField()

    def validate(self, data):
        try:
            course = models.Course.objects.get(id=data['course_id'])
        except models.Course.DoesNotExist:
            raise serializers.ValidationError("course not doesn't exist")

        try:
            student = models.Student.objects.get(id=data['student_id'])
        except models.Student.DoesNotExist:
            raise serializers.ValidationError("student doesn't exist")
        data['student'] = student
        data['course'] = course
        return data

    def create(self, validated_data):
        with transaction.atomic():
            payment = models.Payment.objects.create(
                student=validated_data['student'],
                course=validated_data['course'],
                paid=0,
                debt=validated_data['course'].price,
                is_debt=True,
            )
            return payment
        
    
class PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            'course', 'paid', 'debt', 'is_debt'
        ]
        extra_kwargs = (
            {'paid': {'required': False}, 'debt': {'required': False}}
        )

    
class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = [
            'id', 'name', 'price'
        ]


class PaymentListSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField(method_name='get_student')
    course = serializers.SerializerMethodField(method_name='get_course')

    class Meta:
        model = models.Payment
        fields = [
            'id', 'student', 'course', 'paid', 'debt', 'is_debt'
        ]

    def get_student(self, obj):
        return StudentPaymentSerializer(obj.student).data

    def get_course(self, obj):
        return CourseListSerializer(obj.course).data