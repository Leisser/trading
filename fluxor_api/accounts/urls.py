from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for viewsets
router = DefaultRouter()

urlpatterns = [
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('register/firebase/', views.FirebaseUserRegistrationView.as_view(), name='firebase-user-register'),
    path('convert-token/', views.convert_token, name='convert-token'),
    path('refresh-token/', views.refresh_token, name='refresh-token'),
    path('logout/', views.logout, name='logout'),
    
    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    
    # Session management endpoints
    path('sessions/', views.UserSessionsView.as_view(), name='user-sessions'),
    path('sessions/<int:session_id>/revoke/', views.revoke_session, name='revoke-session'),
    path('sessions/revoke-all/', views.revoke_all_sessions, name='revoke-all-sessions'),
    
    # Verification endpoints
    path('verification/documents/', views.VerificationDocumentsView.as_view(), name='verification-documents'),
    path('verification/status/', views.verification_status, name='verification-status'),
    
    # Include router URLs
    path('', include(router.urls)),
]