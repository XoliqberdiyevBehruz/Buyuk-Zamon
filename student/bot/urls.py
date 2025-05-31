from django.urls import path, include

from student.bot import views

urlpatterns = [
        # path('user/create/', views.StudentCreateApiView.as_view(), name='user create'),
        path('bot/user/get/', views.StudentGetPhoneNumberApiView.as_view()),
        # path('payment/create/', views.PaymentCreateApiView.as_view()),
        path('bot/payment/get/', views.PaymentGetApiView.as_view()),
        path('bot/user/<int:id>/total_price/add/', views.UserTotalPriceUpdateApiView.as_view()),
        path('bot/user/<str:phone_number>/', views.StudentGetNumberApiView.as_view()),
        path('bot/user/<int:id>/join_group/', views.StudentJoinTelegramGroupApiView.as_view()),
        path('bot/verify_user/', views.VerifyStudentApiView.as_view()),
        path('bot/check_group_joined/<int:id>/', views.CheckGroupStudentApiView.as_view()),
]