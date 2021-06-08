from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authtoken.views import obtain_auth_token


schema_view = get_schema_view(openapi.Info(title='Brain API', default_version='pre-alpha'))

# noinspection PyUnresolvedReferences
urlpatterns = [
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns.extend([
    path('users/', include('django.contrib.auth.urls')),
    path('token', obtain_auth_token, name='api_token_auth'),
    path('', include('brain.budgets.urls')),
])
