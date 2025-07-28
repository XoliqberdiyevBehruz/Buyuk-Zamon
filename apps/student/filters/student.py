from django.db.models import Q

import django_filters

from apps.student import models 


class StudentFilter(django_filters.FilterSet):
    is_debt = django_filters.BooleanFilter(method='filter_is_debt')
    a_to_z = django_filters.BooleanFilter(method='filter_a_to_z')
    search = django_filters.CharFilter(method='filter_search')
    month = django_filters.CharFilter(field_name='month')
    status = django_filters.CharFilter(field_name='status')
    year = django_filters.CharFilter(method='filter_year')

    class Meta:
        model = models.Student
        fields = [
            'is_debt', 'a_to_z', 'search', 'month', 'status', 'year'
        ]

    def filter_year(self, queryset, name, value):
        return queryset.filter(student_id_time__year=value)

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
    

class StudentGroupFilter(django_filters.FilterSet):
    student_status = django_filters.CharFilter(method="filter_by_student_status")

    class Meta:
        model = models.Student
        fields = [
            'student_status',
        ]

    def filter_by_student_status(self, queryset, name, value):
        if value == "debt":
            return queryset.filter(
                is_debt=True,
            )
        elif value == "paid":
            return queryset.filter(
                is_debt=False,
            ).distinct()
        elif value == "study":
            return queryset.filter(
                type='study'
            )
        elif value == "graduate":
            return queryset.filter(
                type="graduate"
            )
        elif value == "blacklist":
            return queryset.filter(
                is_blacklist=True
            )
        else:
            return queryset