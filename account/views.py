from django.db.models import Q

from rest_framework import status, generics, permissions, parsers, views
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from account import serializers, models, filters


class StudentCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.StudentCreateSerializer
    queryset = models.Student.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        return Response({'message': True, 'id': student.id}, status=status.HTTP_201_CREATED)

class StudentGetPhoneNumberApiView(generics.GenericAPIView):
    serializer_class = serializers.UserGetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            student = models.Student.objects.get(
                full_name=data['full_name'], 
                phone_number=data['phone_number'], 
                card_number=data['card_number']
            )
            return Response({
                "message": True,
                "id": student.id,
                "telegram_link": student.telegram_link
            }, status=status.HTTP_200_OK)
        except models.Student.DoesNotExist:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)


class PaymentCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.PaymentCreateSerializer
    queryset = models.Payment.objects.all()


class PaymentGetApiView(generics.GenericAPIView):
    serializer_class = serializers.PaymentGetSerializer
    queryset = models.Payment.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        payment = models.Payment.objects.filter(
            payment_id=data['payment_id'], user_id=data['student_id']
        ).first()

        if payment:
            return Response({
                'payment_id': payment.payment_id,
                'user': payment.user.id,
                'price': payment.price
            }, status=status.HTTP_200_OK)
        
        return Response({'message': 'payment not found'}, status=status.HTTP_404_NOT_FOUND)


class UserTotalPriceUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.AddTotalPriceSerializer

    def post(self, request, id, *args, **kwargs):
        try:
            user = models.Student.objects.get(id=id)
        except models.Student.DoesNotExist:
            return Response({'message': "not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user.total_price += int(data['total_price'])
        user.save()

        return Response({'message': 'updated'}, status=status.HTTP_200_OK)
    

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