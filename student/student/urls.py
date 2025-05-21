from django.urls import path

from student.student import views


urlpatterns = [
    path('student/list/', views.StudentListApiView.as_view()),
    path('student/add/', views.StudentAddApiView.as_view()),
    path('student/<int:id>/', views.StudentApiView.as_view()),
    path('student/course_statistic/', views.StudentsStatisticsApiView.as_view()),
]