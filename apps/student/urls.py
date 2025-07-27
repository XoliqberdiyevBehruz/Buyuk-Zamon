from django.urls import path, include

from apps.student.views import (
    student, student_group, student_message, telegram_group, notification,
    payment
)

urlpatterns = [
    # student views and serializer api
    path('student/', include(
        [
            path('list/', student.StudentListApiView.as_view()),
            path('add/', student.StudentAddApiView.as_view()),
            path('<int:id>/update/', student.StudentUpdateApiView.as_view()),
            path('<int:id>/', student.StudentDetailApiView.as_view()),
            path('student/course_statistic/', student.StudentsStatisticsApiView.as_view()),
        ]
    )),

    # notification views and serializer api
    path('notification/', include(
        [
            path('list/', notification.NotificationListApiView.as_view()),
        ]
    )),

    # student message views and serializer api
    path('student_message/', include(
        [
            path('send/message/', student_message.StudentSendMessageApiView.as_view()),
            path('list/', student_message.StudentMessageListApiView.as_view()),
        ]
    )),

    # telegram group views and serializer api
    path('telegram_group/', include(
        [
            path('list/<int:id>/', telegram_group.StudentTelegramGroupListSerializer.as_view()),
        ]
    )),

    # student group views and serializer api
    path('student_group/', include(
        [
            path('create/', student_group.GroupCreateApiView.as_view()),
            path('<int:id>/', student_group.GroupDetailApiView.as_view()),
            path('list/', student_group.GroupListApiView.as_view()),
        ]
    )),
    
    # payment 
    path('payment/', include(
        [
            path('add/', payment.PaymentAddApiView.as_view(),),
            path('student/<int:student_id>/payment/list/', payment.PaymentListApiView.as_view()),
            path('<int:payment_id>/update/', payment.PaymentUpdateApiView.as_view()),
            path('images/create/', payment.PaymentImagesCreateApiView.as_view()),
            path('<int:id>/delete/', payment.PaymentDeleteApiView.as_view()),
        ]
    )),
]