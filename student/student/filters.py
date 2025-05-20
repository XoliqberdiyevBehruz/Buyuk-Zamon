from django.db.models import Q

import django_filters

from student import models 


class StudentFilter(django_filters.FilterSet):
    is_debt = django_filters.BooleanFilter(method='filter_is_debt')
    a_to_z = django_filters.BooleanFilter(method='filter_a_to_z')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = models.Student
        fields = [
            'is_debt', 'a_to_z', 'search'
        ]

    def filter_is_debt(self, queryset, name, value):
        if value == True:
            return queryset.filter(is_debt=True)
        elif value == False:
            return queryset.filter(is_debt=False)
        else:
            return queryset.order_by('-created_at')

    def filter_a_to_z(self, queryset, name, value):
        if value == True:
            return queryset.order_by('full_name')
        elif value == False:
            return queryset.order_by('-full_name')
        else:
            return queryset.order_by('-created_at')


    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(full_name__icontains=value) |
            Q(phone_number__icontains=value) |
            Q(contract_number__icontains=value) |
            Q(student_id__icontains=value)
        )
    