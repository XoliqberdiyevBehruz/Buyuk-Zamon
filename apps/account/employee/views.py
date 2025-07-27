from rest_framework import generics, status
from rest_framework.response import Response

from django_filters.rest_framework.backends import DjangoFilterBackend

from apps.account.employee import serializers, pagination, filters
from apps.account import models, permissions


class EmployeeCreateView(generics.CreateAPIView):
    serializer_class = serializers.EmployeeCreateSerializer
    permission_classes = [permissions.IsBossOrEmployee]
    queryset = models.Employee.objects.order_by('-created_at')    


class EmployeeListView(generics.ListAPIView):
    serializer_class = serializers.EmployeeListSerializer
    permission_classes = [permissions.IsBossOrEmployee]
    queryset = models.Employee.objects.all()
    pagination_class = pagination.CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.EmployeeFilter


class EmployeeDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.EmployeeDetailSerializer
    permission_classes = [permissions.IsBossOrEmployee]
    queryset = models.Employee.objects.all()
    lookup_field = 'id'


class EmployeeUpdateView(generics.UpdateAPIView):
    serializer_class = serializers.EmployeeUpdateSerializer
    permission_classes = [permissions.IsBossOrEmployee]
    queryset = models.Employee.objects.all()
    lookup_field = 'id'


class PositionListApiView(generics.ListAPIView):
    serializer_class = serializers.PositionSerializer
    permission_classes = [permissions.IsBossOrEmployee]
    queryset = models.Position.objects.all()


class EmployeeDashboardApiView(generics.ListAPIView):
    serializer_class = serializers.EmployeeDashboardSerializer
    permission_classes =  [permissions.IsBossOrEmployee]
    queryset = models.Employee.objects.all()


class EmployeeSalarCreateyApiView(generics.CreateAPIView):
    serializer_class = serializers.EmployeeSalaryCreateSerializer
    permission_classes = (permissions.IsBossOrEmployee,)
    queryset = models.EmployeeSalary.objects.all()


class EmployeeSalaryListApiView(generics.GenericAPIView):
    serializer_class = serializers.EmployeeSalarySerializer
    permission_classes = (permissions.IsBossOrEmployee,)
    queryset = models.EmployeeSalary.objects.order_by('-date')

    def get(self, request, employee_id):
        employee_salary = self.queryset.filter(employee__id=employee_id)
        serializer = self.get_serializer(employee_salary, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)