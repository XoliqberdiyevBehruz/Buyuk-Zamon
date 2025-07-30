from rest_framework import generics
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.student.serializers import student_group as student_group_serializer
from apps.student.filters.student import StudentFilter
from apps.student import models, tasks
from apps.account import permissions

 
class GroupCreateApiView(generics.GenericAPIView):
    serializer_class = student_group_serializer.GroupCreateSerializer
    queryset = models.StudentGroup.objects.order_by('-created_at')
    permission_classes = [permissions.IsBossOrEmployee]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "group created"}, status=201)
        return Response(serializer.errors, status=400)



class GroupDetailApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsBossOrEmployee]
    serializer_class = student_group_serializer.GroupStudentListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter

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
    queryset = models.StudentGroup.objects.order_by('-created_at')
    serializer_class = student_group_serializer.GroupListSerializer
    