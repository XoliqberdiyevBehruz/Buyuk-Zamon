from datetime import timedelta

from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth

from rest_framework import views
from rest_framework.response import Response

from student import models 
from account import permissions


class IncomeStatisticApiView(views.APIView):
    permission_classes = (permissions.IsBoss,)

    def get(self, request):
        now = timezone.now()
        queryset = models.Payment.objects.all()

        prediot = request.query_params.get('filter', 'current_month')

        if prediot == 'last_week':
            queryset = queryset.filter(payment_time__gte=now - timedelta(days=7), payment_time__lte=now)
        
        elif prediot == 'last_month':
            if now.month == 1:
                year = now.year - 1
                month = 12
            else:
                month = now.month - 1
            queryset = queryset.filter(payment_time__year=year, payment_time__month=month)
        elif prediot == 'last_year':
            queryset = queryset.filter(payment_time__year=now.year - 1)
        
        elif prediot == 'current_month':
            queryset = queryset.filter(payment_time__month=now.month)

        elif prediot == 'current_year':
            queryset = queryset.filter(payment_time__year=now.year)

        elif prediot == 'current_week':
            queryset = queryset.filter(payment_time__range=(now - timedelta(days=7), now))


        income = queryset.aggregate(
            sum=Sum('price')
        )['sum']

        return Response({
            'icome': income
        })
    

class IncomeMonthlyStatisticApiView(views.APIView):
    permission_classes = (permissions.IsBoss, )

    def get(self, request):
        now = timezone.now()

        data = (
            models.Payment.objects
            .annotate(year=ExtractYear('payment_time'), month=ExtractMonth('payment_time')) 
            .values('year', 'month')    
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