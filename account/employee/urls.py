from django.urls import path 

from account.employee import views

urlpatterns = [
    path('employee/create/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/list/', views.EmployeeListView.as_view(), name='employee-list'), 
    path('employee/<int:id>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/<int:id>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
]