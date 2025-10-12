"""
Firebase Authentication Service for Django
Handles Firebase token verification and user management
"""

import firebase_admin
from firebase_admin import credentials, auth
import logging
from typing import Optional, Dict, Any
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import User
import os

logger = logging.getLogger(__name__)

User = get_user_model()

class FirebaseAuthService:
    """
    Service for handling Firebase authentication using Firebase Admin SDK
    """
    
    def __init__(self):
        # Initialize Firebase Admin SDK if not already initialized
        if not firebase_admin._apps:
            try:
                # Get the path to the service account JSON file
                service_account_path = os.path.join(
                    settings.BASE_DIR,
                    'firebase_service_account.json'
                )
                
                if os.path.exists(service_account_path):
                    cred = credentials.Certificate(service_account_path)
                    firebase_admin.initialize_app(cred)
                    logger.info("Firebase Admin SDK initialized successfully")
                else:
                    logger.error(f"Firebase service account file not found at {service_account_path}")
            except Exception as e:
                logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")
        
        self.project_id = "fluxor-434ed"
    
    def verify_firebase_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Firebase ID token and return user information using Firebase Admin SDK
        
        Args:
            id_token: Firebase ID token from client
            
        Returns:
            Dict containing user information if valid, None if invalid
        """
        try:
            # Verify token with Firebase Admin SDK
            decoded_token = auth.verify_id_token(id_token)
            
            # Get user information from the decoded token
            uid = decoded_token.get('uid')
            
            # Fetch additional user information
            user_record = auth.get_user(uid)
            
            return {
                'uid': user_record.uid,
                'email': user_record.email,
                'email_verified': user_record.email_verified,
                'display_name': user_record.display_name,
                'photo_url': user_record.photo_url,
                'phone_number': user_record.phone_number,
                'provider_id': user_record.provider_id if hasattr(user_record, 'provider_id') else None,
                'created_at': user_record.user_metadata.creation_timestamp if user_record.user_metadata else None,
                'last_login_at': user_record.user_metadata.last_sign_in_timestamp if user_record.user_metadata else None,
            }
                
        except auth.InvalidIdTokenError as e:
            logger.error(f"Invalid Firebase ID token: {str(e)}")
            return None
        except auth.ExpiredIdTokenError as e:
            logger.error(f"Expired Firebase ID token: {str(e)}")
            return None
        except auth.RevokedIdTokenError as e:
            logger.error(f"Revoked Firebase ID token: {str(e)}")
            return None
        except auth.CertificateFetchError as e:
            logger.error(f"Error fetching Firebase certificates: {str(e)}")
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
            
            # Split display name into first and last name
            name_parts = (display_name or '').split(' ', 1) if display_name else ['', '']
            first_name = name_parts[0] if len(name_parts) > 0 else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=None,  # Firebase users don't have Django passwords
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number or '',
                is_active=True,
                firebase_uid=uid
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
            if display_name:
                name_parts = display_name.split(' ', 1)
                first_name = name_parts[0] if len(name_parts) > 0 else ''
                last_name = name_parts[1] if len(name_parts) > 1 else ''
                
                if user.first_name != first_name:
                    user.first_name = first_name
                    updated = True
                if user.last_name != last_name:
                    user.last_name = last_name
                    updated = True
            
            # Update phone number if different
            phone_number = firebase_data.get('phone_number')
            if phone_number and user.phone_number != phone_number:
                user.phone_number = phone_number
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
