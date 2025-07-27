from datetime import timedelta

from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth

from rest_framework import generics, views
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.finance import models
from apps.finance.expence import serializers, filters
from apps.account import permissions


class ExpenceCategoryListApiView(generics.ListAPIView):
    serializer_class = serializers.ExpenceCategoryListSerializer
    queryset = models.ExpenceCategory.objects.all()
    permission_classes = (permissions.IsBoss,)


class ExpenceCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.ExpenceAddSerializer
    queryset = models.Expence.objects.all()
    permission_classes = (permissions.IsBoss,)


class ExpenceListApiView(generics.ListAPIView):
    serializer_class = serializers.ExpenceListSerializer
    queryset = models.Expence.objects.all()
    permission_classes = (permissions.IsBoss,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ExpenceFilter


class ExpenceUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.ExpenceUpdateSerializer
    queryset = models.Expence.objects.all()
    permission_classes = (permissions.IsBoss,)
    lookup_field = 'id'


class ExpenceDeleteApiView(generics.DestroyAPIView):
    queryset = models.Expence.objects.all()
    permission_classes = (permissions.IsBoss,)
    lookup_field = 'id'


class ExpenceStatisticApiView(views.APIView):
    permission_classes = (permissions.IsBoss,)

    def get(self, request):
        now = timezone.now()
        period = request.query_params.get('filter', 'current_month')

        queryset = models.Expence.objects.all()

        if period == 'last_week':
            start_date = now - timedelta(days=7)
            queryset = queryset.filter(date__gte=start_date, date__lte=now)

        elif period == 'last_month':
            if now.month == 1:
                year = now.year - 1
                month = 12
            else:
                year = now.year
                month = now.month - 1
            queryset = queryset.filter(date__year=year, date__month=month)

        elif period == 'last_year':
            queryset = queryset.filter(date__year=now.year - 1)
        
        elif period == 'current_month':
            queryset = queryset.filter(date__month=now.month)

        elif period == 'current_year':
            queryset = queryset.filter(date__year=now.year)

        elif period == 'current_week':
            queryset = queryset.filter(date__range=(now - timedelta(days=7), now))
        
        expence = queryset.aggregate(sum=Sum('price'))['sum'] or 0
        return Response({
            "expence": expence  
        })
    

class ExpenceMonthlyStatisticApiView(views.APIView):
    permission_classes = (permissions.IsBoss,)

    def get(self, request):
        data = (
            models.Expence.objects
            .annotate(year=ExtractYear('date'), month=ExtractMonth('date'))
            .values('year', 'month')  # Bu MUHIM!
            .annotate(total=Sum('price'))
            .order_by('year', 'month')
        )

        result = {}
        for item in data:
            year = item['year']
            month = item['month']
            total = item['total']

            if year not in result:
                result[year] = {i: 0 for i in range(1, 13)}

            result[year][month] = total
        
        return Response(result)
    

class ExpenceCategoryStatisticApiView(views.APIView):
    permission_classes = (permissions.IsBoss, )

    def get(self, request):
        all_sum = models.Expence.objects.aggregate(total=Sum('price'))['total'] or 0

        if all_sum == 0:
            return Response({"message": "Chiqim mavjud emas"})

        category_data = (
            models.Expence.objects
            .values('category__name')
            .annotate(total=Sum("price"))
            .order_by('-total')
        ) 

        result = {}

        for item in category_data:
            category_name = item.get('category__name')
            category_sum = item.get('total')
            percentage = round((category_sum / all_sum) *100, 1)
            result[category_name] = {
                'total': category_sum,
                'percentage': percentage,
            }
            result['sum'] = all_sum
        
        return Response(result)
