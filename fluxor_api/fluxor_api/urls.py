"""
URL configuration for fluxor_api project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Fluxor API",
      default_version='v1',
      description="Bitcoin Trading System API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@fluxor.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def health_check(request):
    """Health check endpoint for Docker health checks"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'fluxor-api',
        'version': '1.0.0'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health_check'),
    path('api/', include('accounts.urls')),
    path('api/', include('wallets.urls')),
    path('api/', include('trades.urls')),
    path('api/', include('blockchain.urls')),
    path('api/trading/', include('trading_engine.urls')),
    path('api/market/', include('market_data.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    # path('api/portfolio/', include('portfolio_management.urls')),
    path('api/risk/', include('risk_management.urls')),
    path('api/compliance/', include('compliance.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 