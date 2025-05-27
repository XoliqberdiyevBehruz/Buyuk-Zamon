import django_filters

from account.models import Employee


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = ['is_left']    
    
