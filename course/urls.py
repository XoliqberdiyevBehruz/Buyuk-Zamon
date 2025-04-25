from django.urls import path, include

from course import views

urlpatterns = [
    path('payment/', include(
        [
            # path('create/', views.PaymentCreateApiView.as_view(), name='payment create api'),
            path('<int:id>/edit/', views.PaymentUpdateApiView.as_view(), name='payment update api'),
            path('list/', views.PaymentListApiView.as_view(), name='payment list api'),
        ]
    )),
    path('course/', include(
        [
            path('list/', views.CourseListApiView.as_view(), name='course list api'),
        ]
    ))
]