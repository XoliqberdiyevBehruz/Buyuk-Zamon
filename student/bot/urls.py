from django.urls import path, include, re_path

from student.bot import views

urlpatterns = [
    path('bot/verify_user/', views.VerifyStudentApiView.as_view()),
    path('bot/user/<int:id>/join_group/', views.StudentJoinTelegramGroupApiView.as_view()),
    path('bot/check_group_joined/<int:id>/', views.CheckGroupStudentApiView.as_view()),
    path('bot/verification_failed/', views.StudentDescriptionCreate.as_view()),
    path('bot/student/<int:id>/update/', views.UpdateStudentApiView.as_view()),
    path('bot/telegram_group/create/', views.TelegramGroupCreateApiView.as_view()),
    path('bot/telegram_group/list/', views.TelegramListApiView.as_view()),
    path('bot/student_group_info/', views.StudentGroupInfoApiView.as_view()),
    re_path(r"^bot/set_telegram_group/(?P<id>-?\d+)/$", views.StudentSetTelegramGroupApiView.as_view()),
    path('bot/student_group_info/<int:id>/', views.StudentSelfGroupInfoApiView.as_view()),
    path('bot/student_group/list/', views.StudentGroupListApiView.as_view()),
    path('bot/student/get_by_tg_id/<int:tg_id>/', views.GetUserByTelegramIdApiView.as_view()),
]