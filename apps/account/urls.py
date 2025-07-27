from django.urls import path, include

from rest_framework_simplejwt.views import  TokenRefreshView

from apps.account.auth.views import LoginApiView

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]