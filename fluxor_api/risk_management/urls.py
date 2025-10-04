from django.urls import path
from .views import (
    RiskAssessmentView, RiskCheckView, PortfolioRiskView,
    RiskAlertsView, RiskSettingsView
)

app_name = 'risk_management'

urlpatterns = [
    # Risk assessment and analysis
    path('assessment/', RiskAssessmentView.as_view(), name='assessment'),
    path('check/', RiskCheckView.as_view(), name='check'),
    path('portfolio/', PortfolioRiskView.as_view(), name='portfolio'),
    
    # Risk alerts and settings
    path('alerts/', RiskAlertsView.as_view(), name='alerts'),
    path('settings/', RiskSettingsView.as_view(), name='settings'),
] 