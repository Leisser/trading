from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, UserProfileView, PasswordChangeView,
    LoginHistoryView, UserSettingsView, KYCUploadView, logout_view,
    NotificationListView, NotificationDetailView, NotificationMarkReadView,
    NotificationMarkAllReadView
)
from .firebase_views import firebase_auth, firebase_verify_token, refresh_firebase_session, firebase_dashboard_auth

app_name = 'accounts'

urlpatterns = [
    # Authentication endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Firebase authentication endpoints
    path('firebase-auth/', firebase_auth, name='firebase_auth'),
    path('firebase-dashboard-auth/', firebase_dashboard_auth, name='firebase_dashboard_auth'),
    path('firebase-verify/', firebase_verify_token, name='firebase_verify'),
    path('firebase-refresh/', refresh_firebase_session, name='firebase_refresh'),
    
    # User profile and settings
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('kyc/upload/', KYCUploadView.as_view(), name='kyc_upload'),
    
    # User activity
    path('login-history/', LoginHistoryView.as_view(), name='login_history'),
    
    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification_detail'),
    path('notifications/<int:pk>/mark_read/', NotificationMarkReadView.as_view(), name='notification_mark_read'),
    path('notifications/mark_all_read/', NotificationMarkAllReadView.as_view(), name='notification_mark_all_read'),
] 