"""
Session Management Service for Firebase Authentication
Handles persistent sessions and automatic token refresh
"""

import logging
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .firebase_auth import firebase_auth_service

logger = logging.getLogger(__name__)
User = get_user_model()


class SessionManager:
    """
    Manages user sessions with Firebase authentication
    """
    
    def __init__(self):
        self.session_timeout = 30 * 24 * 60 * 60  # 30 days in seconds
        self.refresh_threshold = 24 * 60 * 60  # 24 hours in seconds
    
    def create_session(self, user: User, firebase_uid: str = None) -> dict:
        """
        Create a new session for a user
        
        Args:
            user: Django User instance
            firebase_uid: Firebase UID if available
            
        Returns:
            Dict containing access and refresh tokens
        """
        try:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Store session data in cache
            session_data = {
                'user_id': user.id,
                'firebase_uid': firebase_uid,
                'created_at': timezone.now().isoformat(),
                'last_activity': timezone.now().isoformat(),
                'auth_provider': user.auth_provider,
                'is_active': user.is_active
            }
            
            # Cache session for 30 days
            cache.set(
                f"session_{user.id}_{firebase_uid or 'local'}",
                session_data,
                self.session_timeout
            )
            
            # Update user's last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            logger.info(f"Session created for user {user.email}")
            
            return {
                'access': str(access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'avatar': user.avatar,
                    'role': user.role,
                    'is_active': user.is_active,
                    'email_verified': user.email_verified,
                    'phone_number': user.phone_number,
                    'auth_provider': user.auth_provider,
                    'firebase_uid': user.firebase_uid,
                    'created_at': user.date_joined.isoformat(),
                    'last_login': user.last_login.isoformat() if user.last_login else None
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create session for user {user.email}: {str(e)}")
            raise
    
    def refresh_session(self, user: User, refresh_token: str) -> dict:
        """
        Refresh a user's session
        
        Args:
            user: Django User instance
            refresh_token: Current refresh token
            
        Returns:
            Dict containing new access and refresh tokens
        """
        try:
            # Validate refresh token
            token = RefreshToken(refresh_token)
            
            # Check if user is still active
            if not user.is_active:
                raise TokenError("User account is inactive")
            
            # Generate new tokens
            new_refresh = RefreshToken.for_user(user)
            new_access_token = new_refresh.access_token
            
            # Update session data
            session_data = cache.get(f"session_{user.id}_{user.firebase_uid or 'local'}")
            if session_data:
                session_data['last_activity'] = timezone.now().isoformat()
                cache.set(
                    f"session_{user.id}_{user.firebase_uid or 'local'}",
                    session_data,
                    self.session_timeout
                )
            
            # Update last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            logger.info(f"Session refreshed for user {user.email}")
            
            return {
                'access': str(new_access_token),
                'refresh': str(new_refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'avatar': user.avatar,
                    'role': user.role,
                    'is_active': user.is_active,
                    'email_verified': user.email_verified,
                    'phone_number': user.phone_number,
                    'auth_provider': user.auth_provider,
                    'firebase_uid': user.firebase_uid,
                    'created_at': user.date_joined.isoformat(),
                    'last_login': user.last_login.isoformat() if user.last_login else None
                }
            }
            
        except TokenError as e:
            logger.warning(f"Invalid refresh token for user {user.email}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to refresh session for user {user.email}: {str(e)}")
            raise
    
    def validate_session(self, user: User, firebase_uid: str = None) -> bool:
        """
        Validate if a user's session is still active
        
        Args:
            user: Django User instance
            firebase_uid: Firebase UID if available
            
        Returns:
            True if session is valid, False otherwise
        """
        try:
            # Check if user is still active
            if not user.is_active:
                return False
            
            # Check session in cache
            session_data = cache.get(f"session_{user.id}_{firebase_uid or 'local'}")
            if not session_data:
                return False
            
            # Check if session has expired
            last_activity = datetime.fromisoformat(session_data['last_activity'])
            if timezone.now() - last_activity > timedelta(seconds=self.session_timeout):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate session for user {user.email}: {str(e)}")
            return False
    
    def invalidate_session(self, user: User, firebase_uid: str = None) -> None:
        """
        Invalidate a user's session
        
        Args:
            user: Django User instance
            firebase_uid: Firebase UID if available
        """
        try:
            # Remove session from cache
            cache.delete(f"session_{user.id}_{firebase_uid or 'local'}")
            
            # Add token to blacklist if using JWT blacklist
            # This would require django-rest-framework-simplejwt[blacklist]
            
            logger.info(f"Session invalidated for user {user.email}")
            
        except Exception as e:
            logger.error(f"Failed to invalidate session for user {user.email}: {str(e)}")
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions
        
        Returns:
            Number of sessions cleaned up
        """
        try:
            # This would require a more sophisticated implementation
            # For now, we rely on cache TTL
            logger.info("Session cleanup completed (handled by cache TTL)")
            return 0
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired sessions: {str(e)}")
            return 0
    
    def get_user_sessions(self, user: User) -> list:
        """
        Get all active sessions for a user
        
        Args:
            user: Django User instance
            
        Returns:
            List of active sessions
        """
        try:
            # This would require storing session metadata
            # For now, return basic info
            return [{
                'user_id': user.id,
                'last_activity': user.last_login.isoformat() if user.last_login else None,
                'auth_provider': user.auth_provider
            }]
            
        except Exception as e:
            logger.error(f"Failed to get sessions for user {user.email}: {str(e)}")
            return []


# Global session manager instance
session_manager = SessionManager()
