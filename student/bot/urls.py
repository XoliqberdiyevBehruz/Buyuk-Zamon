from django.urls import path, include

from student.bot import views

urlpatterns = [
        path('bot/user/get/', views.StudentGetPhoneNumberApiView.as_view()),
        path('bot/payment/get/', views.PaymentGetApiView.as_view()),
        path('bot/user/<int:id>/total_price/add/', views.UserTotalPriceUpdateApiView.as_view()),
        path('bot/user/<str:phone_number>/', views.StudentGetNumberApiView.as_view()),
        path('bot/user/<int:id>/join_group/', views.StudentJoinTelegramGroupApiView.as_view()),
        path('bot/verify_user/', views.VerifyStudentApiView.as_view()),
        path('bot/check_group_joined/<int:id>/', views.CheckGroupStudentApiView.as_view()),
        path('bot/verification_failed/', views.StudentDescriptionCreate.as_view()),
        path('bot/get_user_by_id/<int:id>/', views.StudentGetByIdApiView.as_view()),
        path('bot/student/<int:id>/update/', views.UpdateStudentApiView.as_view()),
]