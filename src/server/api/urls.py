from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .v1 import urls as urls_v1

API_TITLE = 'Парсер транзакций API'

schema_view_v1 = get_schema_view(
    openapi.Info(title=API_TITLE, default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path('api/v1/', include(urls_v1.urlpatterns))
    ],
)

urlpatterns = [
    path('v1/', include((urls_v1, 'api_v1'))),

    re_path(
        r'v1/swagger(?P<format>\.json|\.yaml)$',
        schema_view_v1.without_ui(cache_timeout=0),
        name='schema-json_v1',
    ),
    re_path(
        r'v1/swagger/',
        schema_view_v1.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui_v1'
    ),
    re_path(
        r'v1/redoc/$',
        schema_view_v1.with_ui('redoc', cache_timeout=0),
        name='schema-redoc_v1',
    ),
]
