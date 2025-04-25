from django.db.models import Q

import django_filters

from course import models 


class PaymentFilter(django_filters.FilterSet):
    is_debt = django_filters.BooleanFilter(method='filter_by_is_debt')
    a_to_z = django_filters.BooleanFilter(method='filter_by_a_to_z')
    search = django_filters.CharFilter(method='filter_by_search')

    class Meta:
        model = models.Payment
        fields = ['is_debt', 'a_to_z', 'search']

    def filter_by_is_debt(self, queryset, name, value):
        if value == True:
            return queryset.filter(
                is_debt=True
            )
        elif value == False:
            return queryset.filter(
                is_debt=False
            )
        else:
            return queryset
        
    def filter_by_a_to_z(self, queryset, name, value):
        if value == True:
            return queryset.order_by(
                'student__last_name'
            )
        elif value == False:
            return queryset.order_by(
                '-student__last_name'
            )
        else:
            return queryset
        
    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(student__first_name__icontains=value) |
            Q(student__last_name__icontains=value) |
            Q(student__phone_number__icontains=value)
        ).distinct()