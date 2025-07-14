from django.db.models import Sum
from django.shortcuts import get_object_or_404

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
    

class GroupCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.GroupCreateSerializer
    queryset = models.StudentGroup.objects.all()
    permission_classes = [permissions.IsBossOrEmployee]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "group created"}, status=201)
        return Response(serializer.errors, status=400)


class FilterStudentForAddGroupApiView(views.APIView):
    permission_classes = [permissions.IsBossOrEmployee]

    def get(self, request):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        student_type = self.request.query_params.get('type', 'new')
        if not start_date or not end_date:
            return Response({"message": "start_date and end_date query is required"}, status=400)
        
        queryset = models.Student.objects.filter(
            student_id_time__range=(start_date, end_date), type=student_type
        )
        serializer = serializers.GroupAddStudentListSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
    

class GroupDetailApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsBossOrEmployee]
    serializer_class = serializers.GroupStudentListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.StudentGroupFilter

    def get(self, request, id):
        try:
            group = models.StudentGroup.objects.get(id=id)
            students = group.students
            serializer = self.serializer_class(self.filter_queryset(students), many=True)
            return Response(serializer.data, status=200)
        except models.StudentGroup.DoesNotExist:
            return Response({"message": 'group not found'}, status=404)


class GroupListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsBossOrEmployee]
    queryset = models.StudentGroup.objects.all()
    serializer_class = serializers.GroupListSerializer
    

class StudentTelegramGroupListSerializer(views.APIView):
    permission_classes = [permissions.IsBossOrEmployee]

    def get(self, request, id):
        student = get_object_or_404(models.Student, id=id)
        telegram_groups = models.TelegramGroup.objects.filter(students=student)
        serializer = serializers.StudentTelegramGroupsSerializer(telegram_groups, many=True)
        return Response(serializer.data, status=200)
    