from django.urls import path, include

from student.payment import views

urlpatterns = [
    path('payments/add/', views.PaymentAddApiView.as_view(),),
    path('payments/student/<int:student_id>/payment/list/', views.PaymentListApiView.as_view()),
    path('payments/<int:payment_id>/update/', views.PaymentUpdateApiView.as_view()),
    path('payments/<int:id>/delete/', views.PaymentDeleteApiView.as_view()),
    path('payments/images/create/', views.PaymentImagesCreateApiView.as_view()),
]