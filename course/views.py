from rest_framework import generics, permissions, status, pagination
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from course import models, serializers, filters


class PaymentCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.PaymentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.PaymentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'created': True, 'error': None}, status=status.HTTP_201_CREATED)
        return Response({'created': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class PaymentUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.PaymentUpdateSerializer
    queryset = models.Payment
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class CourseListApiView(generics.ListAPIView):
    serializer_class = serializers.CourseListSerializer
    queryset = models.Course.objects.order_by('-created_at')
    permission_classes = [permissions.IsAuthenticated]


class PaymentListApiView(generics.ListAPIView):
    serializer_class = serializers.PaymentListSerializer
    queryset = models.Payment.objects.order_by('-created_at')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.PaymentFilter
