from django.db.models import Sum

from rest_framework import generics, status, parsers, views
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from student.student import serializers, filters
from student import models, tasks
from account import permissions

from django.conf import settings


class StudentListApiView(generics.ListAPIView):
    queryset = models.Student.objects.order_by('-created_at').select_related('employee')
    serializer_class = serializers.StudentListSerializer
    permission_classes = [permissions.IsBossOrEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.StudentFilter


class StudentAddApiView(generics.CreateAPIView):
    serializer_class = serializers.StudentAddSerializer
    queryset = models.Student
    permission_classes = [permissions.IsBossOrEmployee]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]


class StudentApiView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.StudentDetailSerializer
    queryset = models.Student
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

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
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
        queryset = models.Student.objects.all()        
        if query_param:
            queryset = queryset.filter(month=query_param)
            
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


class NotificationListApiView(generics.ListAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationListSerializer
    permission_classes = [permissions.IsBossOrEmployee]
    

class StudentSendMessageApiView(generics.GenericAPIView):
    serializer_class = serializers.StudentSendMessageSerializer
    queryset = models.Student.objects.all()
    permission_classes = [permissions.IsBossOrEmployee]

    def post(self, request):
        serializer = serializers.StudentSendMessageSerializer(data=request.data)
        if serializer.is_valid():
            for id in serializer.data.get('ids'):
                tasks.send_telegram_message.delay(settings.BOT_TOKEN, id, serializer.data.get('message'))
            return Response({"message": "send"}, status=status.HTTP_200_OK)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)