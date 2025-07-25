from django.shortcuts import get_object_or_404

from rest_framework import generics, status, parsers, views
from rest_framework.response import Response

from student import models
from student.bot import serializers

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


class StudentGetNumberApiView(views.APIView):
    def get(self, request, phone_number):
        student = models.Student.objects.filter(phone_number__icontains=phone_number).first()
        if not student:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({
                "message": True,
                "id": student.id,
                "full_name": student.full_name,
                "course_price": student.course_price,
                "tariff": student.tariff,
                "paid": student.paid,
                "debt": student.debt,
                "telegram_link": student.telegram_link
            }, status=status.HTTP_200_OK)


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
    

class StudentJoinTelegramGroupApiView(views.APIView):
    def get(self, request, id):
        try:
            student = models.Student.objects.get(id=id)
        except models.Student.DoesNotExist:
            return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        student.group_joined = True
        student.save()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)
    

class VerifyStudentApiView(views.APIView):
    def get(self, request):
        phone = request.query_params.get('phone')
        full_name = request.query_params.get('full_name')
        contract_number = request.query_params.get('contract_number')

        if phone and full_name and contract_number:
            student = models.Student.objects.filter(full_name__iexact=full_name,contract_number=contract_number,phone_number__icontains=phone).first()
            if student:
                return Response(
                    {
                        'id': student.id,
                        'status': student.status,
                        'type': student.type,
                    }
                )
            else:
                return Response({"message": "student not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message':'query params is required!'}, status=status.HTTP_400_BAD_REQUEST)
    

class CheckGroupStudentApiView(views.APIView):
    def get(self, request, id):
        try:
            student = models.Student.objects.get(id=id)
        except models.Student.DoesNotExist:
            return Response({"message": "student not found"}, status=status.HTTP_404_NOT_FOUND)
        joined = student.group_joined
        if student.group_joined == False:
            student.group_joined = True
            student.save()
        return Response({
            'joined': joined
        })


class StudentDescriptionCreate(generics.GenericAPIView):
    serializer_class = serializers.StudentDescriptionSerializer
    queryset = models.Notification.objects.all()

    def post(self, request):
        serializer = serializers.StudentDescriptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentGetByIdApiView(views.APIView):
    def get(self, request, id):
        try:
            student = models.Student.objects.get(id=id)
        except models.Student.DoesNotExist:
            return Response({"message": "student not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "id": student.id,
            "full_name": student.full_name,
            "contract_number": student.contract_number,
            "tariff": student.tariff,
            "course_price": student.course_price,
            "paid": student.paid,
            "debt": student.debt
        }, status=status.HTTP_200_OK)
    

class UpdateStudentApiView(generics.UpdateAPIView):
    serializer_class = serializers.StudentUpdateSerializer
    lookup_field = 'id'
    queryset = models.Student.objects.all()
    


class TelegramGroupCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.TelegramGroupCreateSerializer
    queryset = models.TelegramGroup.objects.all()


class TelegramListApiView(generics.ListAPIView):
    queryset = models.TelegramGroup.objects.all()
    serializer_class = serializers.TelegramGroupSerializer
    pagination_class = None


class StudentGroupInfoApiView(views.APIView):
    def get(self, request):
        group = models.StudentGroup.objects.order_by('created_at').last()
        return Response({
            "name": group.group_name,
            "start_date": group.start_date
        })


class StudentSetTelegramGroupApiView(generics.GenericAPIView):
    serializer_class = serializers.StudentSetTelegramGroupSerializer
    queryset = models.TelegramGroup.objects.all()

    def put(self, request, id):
        student = get_object_or_404(models.TelegramGroup, group_id=id)
        serializer = self.serializer_class(student, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "add"}, status=200)
        return Response(serializer.errors, status=400)


class StudentSelfGroupInfoApiView(views.APIView):
    def get(self, request, id):
        student = get_object_or_404(models.Student, id=id)
        group = models.StudentGroup.objects.filter(students=student).order_by('created_at').last()
        return Response({
            "start_date": group.start_date,
            'name': group.group_name
        })

class StudentGroupListApiView(views.APIView):
    def get(self, request):
        groups = models.StudentGroup.objects.all()
        serializer = serializers.StudentGroupListSerializer(groups, many=True)
        return Response(serializer.data)


class GetUserByTelegramIdApiView(views.APIView):
    def get(self, request, tg_id):
        student = get_object_or_404(models.Student, telegram_id=tg_id)
        return Response({
            "id": student.id,
            "telegram_id": student.telegram_id,
            "status": student.status,
            "type": student.type,
            'group': models.StudentGroup.objects.filter(students=student).first().name
        })
    

class StudentMessageCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.StudentMessageCreateSerializer
    queryset = models.StudentMessage.objects.all()
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True}, status=200)
        return Response(serializer.errors, status=400)
    

class StudentChangeStudyStatusApiView(views.APIView):
    def post(self, request, telegram_id):
        student = get_object_or_404(models.Student, telegram_id=telegram_id)
        student.study_type = "online"
        student.save()
        return Response({"success": True, "message": "student study online"}, status=200)


class GetTelegramChannelByTypeApiView(views.APIView):
    def get(self, request, type):
        telegram_group = get_object_or_404(models.TelegramGroup, type=type)
        return Response(
            {
                'id': telegram_group.group_id
            },
            status=status.HTTP_200_OK
        )