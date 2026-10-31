from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Bosh sahifaga kirganda to'g'ridan-to'g'ri Swagger UI ga yo'naltirish
    path('', RedirectView.as_view(url='/api/schema/swagger-ui/', permanent=False)),

    # Django Admin
    path('admin/', admin.site.urls),

    # Omborxona API
    path('api/v1/warehouse/', include('warehouse.urls')),
    path('api/', include('warehouse.urls')),

    # Swagger / OpenAPI hujjatlari
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
