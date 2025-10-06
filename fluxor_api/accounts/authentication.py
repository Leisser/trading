from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .models import UserSession
from django.utils import timezone

User = get_user_model()


class TokenAuthentication(BaseAuthentication):
    """
    Custom token authentication for Fluxor API
    """
    
    def authenticate(self, request):
        """
        Authenticate user using access token
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return None
        
        # Check if header starts with 'Bearer '
        if not auth_header.startswith('Bearer '):
            return None
        
        # Extract token
        token = auth_header.replace('Bearer ', '')
        
        try:
            # Find active session with this token
            session = UserSession.objects.select_related('user').get(
                access_token=token,
                is_active=True,
                revoked_at__isnull=True
            )
            
            # Check if session is expired
            if session.is_expired():
                # Mark session as inactive
                session.is_active = False
                session.save()
                raise AuthenticationFailed('Token has expired')
            
            # Update last used timestamp
            session.last_used_at = timezone.now()
            session.save()
            
            # Return user and session
            return (session.user, session)
            
        except UserSession.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')
    
    def authenticate_header(self, request):
        """
        Return the authentication header
        """
        return 'Bearer'


class FirebaseAuthentication(BaseAuthentication):
    """
    Firebase token authentication (for direct Firebase token usage)
    """
    
    def authenticate(self, request):
        """
        Authenticate user using Firebase token
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return None
        
        # Check if header starts with 'Firebase '
        if not auth_header.startswith('Firebase '):
            return None
        
        # Extract token
        firebase_token = auth_header.replace('Firebase ', '')
        
        try:
            # Verify Firebase token
            import firebase_admin
            from firebase_admin import auth as firebase_auth
            
            # Initialize Firebase Admin SDK if not already done
            if not firebase_admin._apps:
                from firebase_admin import credentials
                import os
                
                cred = credentials.Certificate({
                    "type": "service_account",
                    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
                    "private_key": os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n'),
                    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                })
                firebase_admin.initialize_app(cred)
            
            # Verify the token
            decoded_token = firebase_auth.verify_id_token(firebase_token)
            firebase_uid = decoded_token['uid']
            
            # Get user by Firebase UID
            try:
                user = User.objects.get(firebase_uid=firebase_uid)
                return (user, None)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found')
                
        except Exception as e:
            raise AuthenticationFailed(f'Firebase authentication failed: {str(e)}')
    
    def authenticate_header(self, request):
        """
        Return the authentication header
        """
        return 'Firebase'
