from django.db.models import Q

from rest_framework import status, generics, permissions, parsers, views
from rest_framework.response import Response

from account import serializers, models


class StudentCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.StudentCreateSerializer
    queryset = models.Student

    def post(self, request):
        serializer = serializers.StudentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': True,
                             "id":serializer.data.student.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentGetPhoneNumberApiView(generics.GenericAPIView):
    serializer_class = serializers.UserGetSerializer

    def post(self, request):
        serializer = serializers.UserGetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            student = models.Student.objects.filter(
                Q(full_name__icontains=data.get('full_name', None)) |
                Q(phone_number__icontains=data.get('phone_number', None)) |
                Q(card_number__icontains=data.get('card_number', None)) 
            )
            return Response({
                "message": True,
                "id":student.id,
                "telegram_link":student.telegram_link
            }, status=status.HTTP_200_OK)
    

class PaymentCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.PaymentCreateSerializer
    queryset = models.Payment
    


class PaymentGetApiView(generics.GenericAPIView):
    serializer_class = serializers.PaymentGetSerializer
    queryset = models.Payment

    def post(self, request):
        serializer = serializers.PaymentGetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            payment = models.Payment.objects.filter(payment_id=data['payment_id'], user__id=data['student_id']).first()
            if payment:
                return Response(
                    {'payment_id': payment.payment_id, 'user': payment.user.id, 'price': payment.price}
                )
            return Response({'message': 'payment not found'}, status=status.HTTP_404_NOT_FOUND)


class UserTotalPriceUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.AddTotalPriceSerializer
    
    def post(self, request, user_id):
        try:
            user = models.Student.objects.get(id=user_id)
        except models.Student.DoesNotExist:
            return Response({'message': "not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.AddTotalPriceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            user.total_price += data['total_price']
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class StudentListApiView(generics.ListAPIView):
    queryset = models.Student.objects.order_by('-created_at')
    serializer_class = serializers.StudentListSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentAddApiView(generics.CreateAPIView):
    serializer_class = serializers.StudentAddSerializer
    queryset = models.Student
    permission_classes = [permissions.IsAuthenticated]
    