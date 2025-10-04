from django.urls import path
from .views import (
    ComplianceCheckView, ComplianceReportView, SuspiciousActivityView,
    RegulatoryComplianceView, ComplianceSettingsView, ComplianceDocumentUploadView
)

app_name = 'compliance'

urlpatterns = [
    # Compliance checks and reports
    path('check/', ComplianceCheckView.as_view(), name='check'),
    path('report/', ComplianceReportView.as_view(), name='report'),
    path('suspicious-activity/', SuspiciousActivityView.as_view(), name='suspicious_activity'),
    
    # Regulatory compliance and settings
    path('regulatory/', RegulatoryComplianceView.as_view(), name='regulatory'),
    path('settings/', ComplianceSettingsView.as_view(), name='settings'),
    path('documents/upload/', ComplianceDocumentUploadView.as_view(), name='document_upload'),
] 