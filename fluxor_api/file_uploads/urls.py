from django.urls import path
from .views import (
    KYCUploadCreateView,
    KYCUploadListView,
    KYCUploadDetailView,
    kyc_upload_status,
    bulk_kyc_upload
)

app_name = 'file_uploads'

urlpatterns = [
    # KYC Upload endpoints
    path('kyc/upload/', KYCUploadCreateView.as_view(), name='kyc_upload'),
    path('kyc/uploads/', KYCUploadListView.as_view(), name='kyc_upload_list'),
    path('kyc/uploads/<int:pk>/', KYCUploadDetailView.as_view(), name='kyc_upload_detail'),
    path('kyc/status/', kyc_upload_status, name='kyc_upload_status'),
    path('kyc/bulk-upload/', bulk_kyc_upload, name='bulk_kyc_upload'),
]
