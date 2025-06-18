from django.urls import path

from student.student import views


urlpatterns = [
    path('student/list/', views.StudentListApiView.as_view()),
    path('student/add/', views.StudentAddApiView.as_view()),
    path('student/<int:id>/', views.StudentApiView.as_view()),
    path('student/course_statistic/', views.StudentsStatisticsApiView.as_view()),
    path('notification/list/', views.NotificationListApiView.as_view()),
    path('student/send/message/', views.StudentSendMessageApiView.as_view()),

    path('group/create/', views.GroupCreateApiView.as_view()),
    path('group/filter_students/', views.FilterStudentForAddGroupApiView.as_view()),
    path('group/<int:id>/', views.GroupDetailApiView.as_view()),
    path('group/list/', views.GroupListApiView.as_view()),
]