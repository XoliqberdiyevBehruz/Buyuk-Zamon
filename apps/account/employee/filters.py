import django_filters

from apps.account.models import Employee


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = ['is_left']    
    
