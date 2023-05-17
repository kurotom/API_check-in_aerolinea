from django.contrib import admin
from django.urls import path, include
from utils.views import error_400, error_404, error_500

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Simulación check-in Aerolínea",
        default_version="0.1",
        description="Check-in automático de pasajeros.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=''),
        license=openapi.License(name='GPL-3.0 License')
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path(
        'doc/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-redoc'
    ),
]

handler400 = error_400
handler404 = error_404
handler500 = error_500
