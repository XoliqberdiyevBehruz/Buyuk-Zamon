from django.urls import path 

from account.employee import views

urlpatterns = [
    path('employee/create/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/list/', views.EmployeeListView.as_view(), name='employee-list'), 
    path('employee/<int:id>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/<int:id>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('position/list/', views.PositionListApiView.as_view(), name='position-list'),

    path('employee/salary/add/', views.EmployeeSalarCreateyApiView.as_view()),
    path('employee/salary/list/<int:employee_id>/', views.EmployeeSalaryListApiView.as_view(), name='employee-salary-list'),
]