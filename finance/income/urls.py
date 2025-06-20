from django.urls import path, include

from finance.income import views 

urlpatterns = [
    path('income/statistics/', views.IncomeStatisticApiView.as_view()),
    path('income/statistics/monthly/', views.IncomeMonthlyStatisticApiView.as_view()),
]