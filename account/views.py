from rest_framework import status, generics, permissions, parsers
from rest_framework.response import Response

from account import serializers, models


class StudentCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.StudentCreateSerializer
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def post(self, request):
        serializer = serializers.StudentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"created": True, "error": None}, status=status.HTTP_201_CREATED)
        return Response({"created": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class StudentDetailApiView(generics.GenericAPIView):
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, student_id):
        try:
            student = models.Student.objects.get(id=student_id)
        except models.Student.DoesNotExist:
            return Response({"error": "student not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class StudentUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    lookup_field = 'id'
    queryset = models.Student
    