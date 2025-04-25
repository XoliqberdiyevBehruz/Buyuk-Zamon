from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Buyuk Zamon Crm API",
      default_version='v1',
      description="Buyuk Zamon Crm Api first version",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="xoliqberdiyevbehruz12@gmail.com"),
      license=openapi.License(name="Repid Agancy"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   url='https://buyuk.zamon.crm.repid.uz'
)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/v1/auth/', include('account.urls')),
   path('api/v1/course/', include('course.urls')),

   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)