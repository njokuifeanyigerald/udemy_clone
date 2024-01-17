from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('payment/', include('payments.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]


from django.contrib import admin
from django.urls import path, include


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="UDEMY API",
      default_version='CodeByGerald v1',
      description="built a real estate api that contains listing, users and realtor with search properties",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="njokuifeanyigerald@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('payment/', include('payments.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]



if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root =settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)