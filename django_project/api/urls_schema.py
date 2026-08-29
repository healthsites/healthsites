"""Schema generator."""

from django.conf.urls import url
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from api.api_views.v2.schema import SchemaView

urlpatterns = [
    url(r'^docs/openapi/', SpectacularAPIView.as_view(), name='openapi-schema'),
    url(r'^docs/', SpectacularSwaggerView.as_view(url_name='openapi-schema'), name='swagger-ui'),
    url(r'^redoc/', SpectacularRedocView.as_view(url_name='openapi-schema'), name='redoc'),
    url(r'^schema/', SchemaView.as_view(), name='schema_view'),
]
