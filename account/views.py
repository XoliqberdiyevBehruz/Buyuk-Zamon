from django.db.models import Q

from rest_framework import status, generics, permissions, parsers, views
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from account import serializers, models, filters


class StudentCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.StudentCreateSerializer
    queryset = models.Student

    def post(self, request):
        serializer = serializers.StudentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            student = serializer.save()
            return Response({'message': True,
                             "id": student.id}, status=status.HTTP_201_CREATED)
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
            ).first()
            if student:
                return Response({
                    "message": True,
                    "id":student.id,
                    "telegram_link":student.telegram_link
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)


class PaymentCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.PaymentCreateSerializer
    queryset = models.Payment

    def post(self, request):
        serializer = serializers.PaymentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


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
    
    def post(self, request, id):
        try:
            user = models.Student.objects.get(id=id)
        except models.Student.DoesNotExist:
            return Response({'message': "not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.AddTotalPriceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            user.total_price += int(data['total_price'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class StudentListApiView(generics.ListAPIView):
    queryset = models.Student.objects.order_by('-created_at')
    serializer_class = serializers.StudentListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.StudentFilter


class StudentAddApiView(generics.CreateAPIView):
    serializer_class = serializers.StudentAddSerializer
    queryset = models.Student
    permission_classes = [permissions.IsAuthenticated]


class StudentApiView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.StudentAddSerializer
    queryset = models.Student
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'