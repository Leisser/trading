"""
Firebase Authentication Service for Django
Handles Firebase token verification and user management
"""

import requests
import logging
from typing import Optional, Dict, Any
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import User

logger = logging.getLogger(__name__)

User = get_user_model()

class FirebaseAuthService:
    """
    Service for handling Firebase authentication
    """
    
    def __init__(self):
        self.project_id = "fluxor-434ed"
        self.verify_url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup"
        self.api_key = "AIzaSyC2EjPY7nG7uFyu6l2ymNlTGxTecOD69gU"
    
    def verify_firebase_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Firebase ID token and return user information
        
        Args:
            id_token: Firebase ID token from client
            
        Returns:
            Dict containing user information if valid, None if invalid
        """
        try:
            # Verify token with Firebase
            response = requests.post(
                self.verify_url,
                params={'key': self.api_key},
                json={'idToken': id_token},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                users = data.get('users', [])
                
                if users:
                    user_data = users[0]
                    return {
                        'uid': user_data.get('localId'),
                        'email': user_data.get('email'),
                        'email_verified': user_data.get('emailVerified', False),
                        'display_name': user_data.get('displayName'),
                        'photo_url': user_data.get('photoUrl'),
                        'phone_number': user_data.get('phoneNumber'),
                        'provider_id': user_data.get('providerId'),
                        'created_at': user_data.get('createdAt'),
                        'last_login_at': user_data.get('lastLoginAt'),
                    }
                else:
                    logger.warning("No user data found in Firebase response")
                    return None
            else:
                logger.error(f"Firebase verification failed: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Error verifying Firebase token: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error verifying Firebase token: {str(e)}")
            return None
    
    def get_or_create_user_from_firebase(self, firebase_data: Dict[str, Any]) -> Optional[User]:
        """
        Get or create Django user from Firebase data
        
        Args:
            firebase_data: User data from Firebase verification
            
        Returns:
            Django User instance or None if creation fails
        """
        try:
            uid = firebase_data.get('uid')
            email = firebase_data.get('email')
            
            if not uid or not email:
                logger.error("Missing required Firebase user data (uid or email)")
                return None
            
            # Try to get existing user by Firebase UID or email
            user = None
            
            # First, try to find by Firebase UID (if stored)
            try:
                user = User.objects.get(firebase_uid=uid)
            except User.DoesNotExist:
                pass
            
            # If not found by UID, try by email
            if not user:
                try:
                    user = User.objects.get(email=email)
                    # Update Firebase UID if not set
                    if not user.firebase_uid:
                        user.firebase_uid = uid
                        user.save(update_fields=['firebase_uid'])
                except User.DoesNotExist:
                    pass
            
            # Create new user if not found
            if not user:
                user = self.create_user_from_firebase(firebase_data)
            
            # Update user data if needed
            if user:
                self.update_user_from_firebase(user, firebase_data)
            
            return user
            
        except Exception as e:
            logger.error(f"Error getting/creating user from Firebase: {str(e)}")
            return None
    
    def create_user_from_firebase(self, firebase_data: Dict[str, Any]) -> Optional[User]:
        """
        Create new Django user from Firebase data
        
        Args:
            firebase_data: User data from Firebase verification
            
        Returns:
            Created Django User instance or None if creation fails
        """
        try:
            uid = firebase_data.get('uid')
            email = firebase_data.get('email')
            display_name = firebase_data.get('display_name')
            email_verified = firebase_data.get('email_verified', False)
            phone_number = firebase_data.get('phone_number')
            
            # Generate a unique username from email
            username = email.split('@')[0] if email else f"firebase_user_{uid}"
            counter = 1
            original_username = username
            
            while User.objects.filter(username=username).exists():
                username = f"{original_username}_{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=None,  # Firebase users don't have Django passwords
                full_name=display_name or '',
                phone_number=phone_number or '',
                is_active=True,
                email_verified=email_verified,
                firebase_uid=uid,
                auth_provider='firebase'
            )
            
            logger.info(f"Created new Firebase user: {user.email}")
            return user
            
        except Exception as e:
            logger.error(f"Error creating user from Firebase: {str(e)}")
            return None
    
    def update_user_from_firebase(self, user: User, firebase_data: Dict[str, Any]) -> None:
        """
        Update Django user with latest Firebase data
        
        Args:
            user: Django User instance
            firebase_data: User data from Firebase verification
        """
        try:
            updated = False
            
            # Update display name if different
            display_name = firebase_data.get('display_name')
            if display_name and user.full_name != display_name:
                user.full_name = display_name
                updated = True
            
            # Update email verification status
            email_verified = firebase_data.get('email_verified', False)
            if user.email_verified != email_verified:
                user.email_verified = email_verified
                updated = True
            
            # Update phone number if different
            phone_number = firebase_data.get('phone_number')
            if phone_number and user.phone_number != phone_number:
                user.phone_number = phone_number
                updated = True
            
            # Update photo URL if available (store in avatar field)
            photo_url = firebase_data.get('photo_url')
            if photo_url and user.avatar != photo_url:
                user.avatar = photo_url
                updated = True
            
            if updated:
                user.save()
                logger.info(f"Updated Firebase user: {user.email}")
                
        except Exception as e:
            logger.error(f"Error updating user from Firebase: {str(e)}")
    
    def authenticate_firebase_user(self, id_token: str) -> Optional[User]:
        """
        Authenticate user with Firebase token
        
        Args:
            id_token: Firebase ID token
            
        Returns:
            Django User instance if authentication successful, None otherwise
        """
        try:
            # Verify token with Firebase
            firebase_data = self.verify_firebase_token(id_token)
            
            if not firebase_data:
                logger.warning("Firebase token verification failed")
                return None
            
            # Get or create user
            user = self.get_or_create_user_from_firebase(firebase_data)
            
            if user and user.is_active:
                logger.info(f"Firebase authentication successful for user: {user.email}")
                return user
            else:
                logger.warning(f"Firebase authentication failed for inactive user: {user.email if user else 'unknown'}")
                return None
                
        except Exception as e:
            logger.error(f"Error in Firebase authentication: {str(e)}")
            return None


# Global instance
firebase_auth_service = FirebaseAuthService()
