from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from wagtail.admin import urls as wagtailadmin_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Bank Webhook API",
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("api/v1/", include("payments.urls")),
]

urlpatterns += [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
