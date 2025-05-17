from rest_framework import generics, views, permissions, status, parsers
from rest_framework.response import Response

from account.employee import serializers, pagination
from account import models


class EmployeeCreateView(generics.CreateAPIView):
    serializer_class = serializers.EmployeeCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Employee.objects.all()    


class EmployeeListView(generics.ListAPIView):
    serializer_class = serializers.EmployeeListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Employee.objects.all()
    pagination_class = pagination.CustomPagination


class EmployeeDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.EmployeeDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Employee.objects.all()
    lookup_field = 'id'


class EmployeeUpdateView(generics.UpdateAPIView):
    serializer_class = serializers.EmployeeUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Employee.objects.all()
    lookup_field = 'id'


class PositionListApiView(generics.ListAPIView):
    serializer_class = serializers.PositionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Position.objects.all()


class EmployeeDashboardApiView(generics.ListAPIView):
    serializer_class = serializers.EmployeeDashboardSerializer
    permission_classes =  [permissions.IsAuthenticated]
    queryset = models.Employee.objects.all()


class EmployeeSalarCreateyApiView(generics.CreateAPIView):
    serializer_class = serializers.EmployeeSalaryCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.EmployeeSalary.objects.all()