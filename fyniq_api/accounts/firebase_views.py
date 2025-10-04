"""
Firebase Authentication Views for Django REST Framework
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
from django.utils import timezone
import logging

from .firebase_auth import firebase_auth_service
from .session_manager import session_manager
from .serializers import UserSerializer

logger = logging.getLogger(__name__)
User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def firebase_auth(request):
    """
    Authenticate user with Firebase ID token
    
    Expected payload:
    {
        "id_token": "firebase_id_token",
        "firebase_user": {
            "uid": "firebase_uid",
            "email": "user@example.com",
            "displayName": "User Name",
            "photoURL": "https://...",
            "emailVerified": true,
            "phoneNumber": "+1234567890"
        }
    }
    """
    try:
        id_token = request.data.get('id_token')
        firebase_user_data = request.data.get('firebase_user', {})
        
        if not id_token:
            return Response(
                {'error': 'Firebase ID token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authenticate with Firebase
        user = firebase_auth_service.authenticate_firebase_user(id_token)
        
        if not user:
            return Response(
                {'error': 'Invalid Firebase token or user not found'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Create persistent session using session manager
        session_data = session_manager.create_session(user, firebase_user_data.get('uid'))
        
        logger.info(f"Firebase authentication successful for user: {user.email}")
        
        return Response({
            'access': session_data['access'],
            'refresh': session_data['refresh'],
            'user': session_data['user'],
            'message': 'Firebase authentication successful - session created'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Firebase authentication error: {str(e)}")
        return Response(
            {'error': 'Authentication failed. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def firebase_dashboard_auth(request):
    """
    Authenticate user with Firebase ID token for dashboard access
    Only allows superusers to access the dashboard
    
    Expected payload:
    {
        "id_token": "firebase_id_token",
        "firebase_user": {
            "uid": "firebase_uid",
            "email": "user@example.com",
            "displayName": "User Name",
            "photoURL": "https://...",
            "emailVerified": true,
            "phoneNumber": "+1234567890"
        }
    }
    """
    try:
        id_token = request.data.get('id_token')
        firebase_user_data = request.data.get('firebase_user', {})
        
        if not id_token:
            return Response(
                {'error': 'Firebase ID token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authenticate with Firebase
        user = firebase_auth_service.authenticate_firebase_user(id_token)
        
        if not user:
            return Response(
                {'error': 'Invalid Firebase token or user not found'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if user is superuser
        if not user.is_superuser:
            logger.warning(f"Dashboard access denied for non-superuser: {user.email}")
            return Response(
                {
                    'error': 'Access denied',
                    'message': 'You do not have the required credentials to access the dashboard. Only superusers are allowed.',
                    'requires_superuser': True
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create persistent session using session manager
        session_data = session_manager.create_session(user, firebase_user_data.get('uid'))
        
        logger.info(f"Dashboard authentication successful for superuser: {user.email}")
        
        return Response({
            'access': session_data['access'],
            'refresh': session_data['refresh'],
            'user': session_data['user'],
            'message': 'Dashboard authentication successful - superuser session created'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Dashboard authentication error: {str(e)}")
        return Response(
            {'error': 'Authentication failed. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def firebase_verify_token(request):
    """
    Verify Firebase token without authentication
    Useful for checking token validity
    """
    try:
        id_token = request.data.get('id_token')
        
        if not id_token:
            return Response(
                {'error': 'Firebase ID token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify token with Firebase
        firebase_data = firebase_auth_service.verify_firebase_token(id_token)
        
        if firebase_data:
            return Response({
                'valid': True,
                'user_data': firebase_data
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'valid': False, 'error': 'Invalid token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    except Exception as e:
        logger.error(f"Firebase token verification error: {str(e)}")
        return Response(
            {'valid': False, 'error': 'Token verification failed'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_firebase_session(request):
    """
    Refresh Firebase session tokens
    """
    try:
        refresh_token = request.data.get('refresh')
        user_id = request.data.get('user_id')
        
        if not refresh_token or not user_id:
            return Response(
                {'error': 'Refresh token and user ID are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Refresh session
        session_data = session_manager.refresh_session(user, refresh_token)
        
        logger.info(f"Session refreshed for user: {user.email}")
        
        return Response({
            'access': session_data['access'],
            'refresh': session_data['refresh'],
            'user': session_data['user'],
            'message': 'Session refreshed successfully'
        }, status=status.HTTP_200_OK)
        
    except TokenError as e:
        logger.warning(f"Invalid refresh token: {str(e)}")
        return Response(
            {'error': 'Invalid refresh token'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        logger.error(f"Session refresh error: {str(e)}")
        return Response(
            {'error': 'Session refresh failed. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
