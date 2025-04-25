from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account import views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('student/', include(
        [
            path('create/', views.StudentCreateApiView.as_view(), name='student create api'),
            path('<int:student_id>/', views.StudentDetailApiView.as_view(), name='get student by id api'),
            path('<int:id>/edit/', views.StudentUpdateApiView.as_view(), name='student update api'),
        ]
    ))
]