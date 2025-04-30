from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account import views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('bot/', include(
        [
            path('user/create/', views.StudentCreateApiView.as_view(), name='user create'),
            path('user/get/', views.StudentGetPhoneNumberApiView.as_view()),
            path('payment/create/', views.PaymentCreateApiView.as_view()),
            path('payment/get/', views.PaymentGetApiView.as_view()),
            path('user/<int:id>/total_price/add/', views.UserTotalPriceUpdateApiView.as_view()),
            path('user/<str:phone_number>/', views.StudentGetNumberApiView.as_view()),
        ]
    )),
    path('crm/', include(
        [
            path('student/list/', views.StudentListApiView.as_view()),
            path('student/add/', views.StudentAddApiView.as_view()),
            path('student/<int:id>/', views.StudentApiView.as_view()),
            path('payment/add/', views.PaymentAddApiView.as_view(),),
            path('student/<int:student_id>/payment/list/', views.PaymentListApiView.as_view()),
            path('payment/<int:payment_id>/update/', views.PaymentUpdateApiView.as_view()),
            path('payment/<int:id>/delete/', views.PaymentDeleteApiView.as_view()),
        ]
    ))
]