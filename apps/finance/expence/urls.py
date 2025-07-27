from django.urls import path, include

from apps.account.employee.views import EmployeeDashboardApiView
from apps.finance.expence import views

urlpatterns = [
    path('employee/salary/list/', EmployeeDashboardApiView.as_view(), name='employee salary list'),
    
    path('expence/create/', views.ExpenceCreateApiView.as_view()),
    path('expence/list/', views.ExpenceListApiView.as_view()),
    path('expence/<int:id>/update/', views.ExpenceUpdateApiView.as_view()),
    path('expence/<int:id>/delete/', views.ExpenceDeleteApiView.as_view()),

    path('expence/statistics/', views.ExpenceStatisticApiView.as_view()),
    path('expence/statistics/monthly/', views.ExpenceMonthlyStatisticApiView.as_view()),
    path('expence/statistics/by_category_percentage/', views.ExpenceCategoryStatisticApiView.as_view()),

    path('expence-category/list/', views.ExpenceCategoryListApiView.as_view()),
]