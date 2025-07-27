from rest_framework import generics, status, parsers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.student import models 
from apps.student.payment import serializers
from apps.account import permissions


class PaymentAddApiView(generics.CreateAPIView):
    serializer_class = serializers.PaymentAddSerializer
    permission_classes = [permissions.IsBossOrEmployee]
    queryset = models.Payment.objects.all()


class PaymentListApiView(generics.GenericAPIView):
    serializer_class = serializers.PaymentListSerializer
    permission_classes = [permissions.IsBossOrEmployee]

    def get(self, request, student_id):
        payments = models.Payment.objects.filter(user__id=student_id).order_by('-created_at')
        serializer = serializers.PaymentListSerializer(data=payments, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.PaymentUpdateSerializer
    permission_classes = [permissions.IsBossOrEmployee]

    def put(self, request, payment_id):
        try:
            payment = models.Payment.objects.get(id=payment_id)
        except models.Payment.DoesNotExist:
            return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        if payment.type == 'naxt':
            serializer = serializers.PaymentUpdateSerializer(instance=payment, data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response({'message': 'you cannot update this payment'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentDeleteApiView(generics.DestroyAPIView):
    queryset = models.Payment.objects.all()
    permission_classes = [permissions.IsBossOrEmployee,]
    lookup_field = 'id'


class PaymentImagesCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.PaymentImagesCreateSerializer
    permission_classes = [permissions.IsBossOrEmployee]
    queryset = models.PaymentImage.objects.all()
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]