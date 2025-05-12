from rest_framework import generics, status, parsers, permissions
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from student.student import serializers, filters
from student import models 

class StudentListApiView(generics.ListAPIView):
    queryset = models.Student.objects.order_by('-created_at').select_related('employee')
    serializer_class = serializers.StudentListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.StudentFilter


class StudentAddApiView(generics.CreateAPIView):
    serializer_class = serializers.StudentAddSerializer
    queryset = models.Student
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]


class StudentApiView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.StudentDetailSerializer
    queryset = models.Student
    permission_classes = [permissions.IsAuthenticated]
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
