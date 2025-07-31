from django.db.models import Sum

from rest_framework import generics, status, parsers, views
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.student.serializers import student as student_serializer
from apps.student.filters import student as student_filter
from apps.student import models
from apps.account import permissions


class StudentListApiView(generics.ListAPIView):
    queryset = models.Student.objects.order_by('-created_at').select_related('employee')
    serializer_class = student_serializer.StudentListSerializer
    permission_classes = [permissions.IsBossOrEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_class = student_filter.StudentFilter 


class StudentAddApiView(generics.CreateAPIView):
    serializer_class = student_serializer.StudentAddSerializer
    queryset = models.Student.objects.all()
    permission_classes = [permissions.IsBossOrEmployee]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]


class StudentDetailApiView(generics.RetrieveAPIView):
    serializer_class = student_serializer.StudentDetailSerializer
    queryset = models.Student.objects.all()
    permission_classes = [permissions.IsBossOrEmployee]
    lookup_field = 'id'


class StudentUpdateApiView(generics.UpdateAPIView):
    serializer_class = student_serializer.StudentUpdateSerializer
    queryset = models.Student.objects.all()
    permission_classes = [permissions.IsBossOrEmployee]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        paid_amount = request.data.get('paid')
        if paid_amount is not None:
            instance.debt = instance.course_price - int(paid_amount)
            if instance.debt <= 0:
                instance.debt = 0
                instance.is_debt = False
        instance.save()
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "status": "success",
            "message": "Student updated!",
            "data": serializer.data
        })
    
    def perform_update(self, serializer):
        serializer.save()


class StudentsStatisticsApiView(views.APIView):
    permission_classes = [permissions.IsBossOrEmployee]

    def get(self, request):
        query_param = request.query_params.get('month')
        query_param_year = request.query_params.get('year')
        queryset = models.Student.objects.all()        
        if query_param:
            queryset = queryset.filter(month=query_param)
        if query_param_year:
            queryset = queryset.filter(student_id_time__year=query_param_year)
        total_price = queryset.aggregate(total_price=Sum('course_price'))['total_price']
        total_paid_price = queryset.aggregate(total_paid_price=Sum('paid'))['total_paid_price']
        total_indebtedness_price = queryset.aggregate(total_indebtedness_price=Sum('debt'))['total_indebtedness_price']
        indebtedness_students_count = queryset.filter(is_debt=True).count()
        paid_students_count = queryset.filter(is_debt=False).count()

        return Response(
            {
                'total_price': total_price,
                'total_paid': total_paid_price,
                'total_indebtedness': total_indebtedness_price,
                'indebtedness_students_count': indebtedness_students_count,
                'paid_students_count': paid_students_count,
            }
        )
    

class StudentServiceAddApiView(generics.CreateAPIView):
    serializer_class = student_serializer.StudentServiceAddSerializer
    queryset = models.Student.objects.all()
    permission_classes = [permissions.IsBossOrEmployee]
