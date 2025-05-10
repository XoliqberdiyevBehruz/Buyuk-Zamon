from django.urls import path, include

from student.payment import views

urlpatterns = [
    path('payment/add/', views.PaymentAddApiView.as_view(),),
    path('payment/student/<int:student_id>/payment/list/', views.PaymentListApiView.as_view()),
    path('payment/<int:payment_id>/update/', views.PaymentUpdateApiView.as_view()),
    path('payment/<int:id>/delete/', views.PaymentDeleteApiView.as_view()),
    path('payment/images/create/', views.PaymentImagesCreateApiView.as_view()),
]