from rest_framework import status, generics, permissions, serializers as rest_serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db import transaction
from .models import User, UserSession, VerificationDocument
from .serializers import (
    UserRegistrationSerializer,
    FirebaseUserRegistrationSerializer,
    TokenConversionSerializer,
    RefreshTokenSerializer,
    UserSerializer,
    UserSessionSerializer,
    VerificationDocumentSerializer
)
import logging

logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    """View for user registration"""
    
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Create new user"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"User registration error: {str(e)}")
            return Response({
                'message': 'Registration failed',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class FirebaseUserRegistrationView(generics.CreateAPIView):
    """View for Firebase user registration with ID verification"""
    
    queryset = User.objects.all()
    serializer_class = FirebaseUserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Create user from Firebase data"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            with transaction.atomic():
                user = serializer.save()
                
                # Create verification documents if KYC upload IDs provided
                kyc_upload_ids = request.data.get('kyc_upload_ids', [])
                if kyc_upload_ids:
                    from file_uploads.models import KYCUpload
                    for upload_id in kyc_upload_ids:
                        try:
                            kyc_upload = KYCUpload.objects.get(id=upload_id, user=user)
                            VerificationDocument.objects.create(
                                user=user,
                                document_type=kyc_upload.document_type,
                                file=kyc_upload.file,
                                file_url=kyc_upload.get_file_url(),
                                file_name=kyc_upload.original_filename,
                                file_size=kyc_upload.file_size,
                                mime_type=kyc_upload.mime_type
                            )
                        except KYCUpload.DoesNotExist:
                            logger.warning(f"KYC upload {upload_id} not found for user {user.id}")
                
                # Backward compatibility: Create verification documents if image URLs provided
                id_images = request.data.get('id_images', {})
                for doc_type, image_url in id_images.items():
                    if image_url:
                        VerificationDocument.objects.create(
                            user=user,
                            document_type=doc_type,
                            file_url=image_url,
                            file_name=f"{doc_type}_{user.id}",
                            file_size=0,  # Will be updated when file is processed
                            mime_type="image/jpeg"
                        )
            
            return Response({
                'message': 'User registered successfully. Please sign in to continue.',
                'user_id': user.id,
                'verification_status': user.verification_status
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Firebase user registration error: {str(e)}")
            return Response({
                'message': 'Registration failed',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def convert_token(request):
    """Convert Firebase token to backend tokens"""
    try:
        serializer = TokenConversionSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        result = serializer.save()
        
        return Response({
            'message': 'Sign in successful',
            'access_token': result['access_token'],
            'refresh_token': result['refresh_token'],
            'user': result['user']
        }, status=status.HTTP_200_OK)
        
    except rest_serializers.ValidationError as e:
        # Handle validation errors with user-friendly messages
        logger.error(f"Token validation error: {str(e)}")
        error_detail = e.detail if hasattr(e, 'detail') else str(e)
        
        # Extract user-friendly message
        if 'token' in error_detail and isinstance(error_detail.get('token'), list):
            error_msg = str(error_detail['token'][0]) if error_detail['token'] else 'Authentication failed'
            
            # Convert technical errors to user-friendly messages
            if 'expired' in error_msg.lower():
                message = 'Your session has expired. Please sign in again.'
            elif 'invalid' in error_msg.lower() or 'failed to initialize' in error_msg.lower():
                message = 'Authentication failed. Please sign in again.'
            elif 'not found' in error_msg.lower():
                message = 'Account not found. Please sign up first.'
            else:
                message = 'Authentication failed. Please try again.'
        else:
            message = 'Authentication failed. Please try again.'
            
        return Response({
            'message': message,
            'error': 'authentication_failed'
        }, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.error(f"Token conversion error: {str(e)}")
        return Response({
            'message': 'An error occurred during sign in. Please try again.',
            'error': 'server_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """Refresh access token using refresh token"""
    try:
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        result = serializer.save()
        
        return Response({
            'message': 'Session refreshed successfully',
            'access_token': result['access_token'],
            'refresh_token': result['refresh_token']
        }, status=status.HTTP_200_OK)
        
    except rest_serializers.ValidationError as e:
        logger.error(f"Token validation error: {str(e)}")
        error_detail = str(e.detail) if hasattr(e, 'detail') else str(e)
        
        # User-friendly messages
        if 'expired' in error_detail.lower():
            message = 'Your session has expired. Please sign in again.'
        elif 'invalid' in error_detail.lower():
            message = 'Invalid session. Please sign in again.'
        else:
            message = 'Session refresh failed. Please sign in again.'
            
        return Response({
            'message': message,
            'error': 'session_error'
        }, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return Response({
            'message': 'An error occurred. Please sign in again.',
            'error': 'server_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for user profile management"""
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        """Update user profile"""
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response({
                'message': 'Profile updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Profile update error: {str(e)}")
            return Response({
                'message': 'Profile update failed',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserSessionsView(generics.ListAPIView):
    """View for listing user sessions"""
    
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserSession.objects.filter(
            user=self.request.user,
            is_active=True
        ).order_by('-created_at')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke_session(request, session_id):
    """Revoke a specific user session"""
    try:
        session = UserSession.objects.get(
            id=session_id,
            user=request.user,
            is_active=True
        )
        
        session.revoke()
        
        return Response({
            'message': 'Session revoked successfully'
        }, status=status.HTTP_200_OK)
        
    except UserSession.DoesNotExist:
        return Response({
            'message': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Session revocation error: {str(e)}")
        return Response({
            'message': 'Failed to revoke session',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke_all_sessions(request):
    """Revoke all user sessions except current one"""
    try:
        current_session_token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
        
        sessions = UserSession.objects.filter(
            user=request.user,
            is_active=True
        ).exclude(access_token=current_session_token)
        
        for session in sessions:
            session.revoke()
        
        return Response({
            'message': f'Revoked {sessions.count()} sessions successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Bulk session revocation error: {str(e)}")
        return Response({
            'message': 'Failed to revoke sessions',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


class VerificationDocumentsView(generics.ListCreateAPIView):
    """View for managing verification documents"""
    
    serializer_class = VerificationDocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return VerificationDocument.objects.filter(
            user=self.request.user
        ).order_by('-uploaded_at')
    
    def create(self, request, *args, **kwargs):
        """Upload verification document"""
        try:
            data = request.data.copy()
            data['user'] = request.user.id
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            document = serializer.save()
            
            return Response({
                'message': 'Document uploaded successfully',
                'document': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Document upload error: {str(e)}")
            return Response({
                'message': 'Document upload failed',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verification_status(request):
    """Get user verification status"""
    try:
        user = request.user
        documents = VerificationDocument.objects.filter(user=user)
        
        return Response({
            'verification_status': user.verification_status,
            'is_verified': user.is_verified,
            'is_fully_verified': user.is_fully_verified(),
            'can_trade': user.can_trade(),
            'documents': VerificationDocumentSerializer(documents, many=True).data,
            'verification_notes': user.verification_notes,
            'submitted_at': user.verification_submitted_at,
            'approved_at': user.verification_approved_at
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Verification status error: {str(e)}")
        return Response({
            'message': 'Failed to get verification status',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user and revoke current session"""
    try:
        # Get current session token
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.replace('Bearer ', '')
            
            # Find and revoke current session
            try:
                session = UserSession.objects.get(
                    access_token=token,
                    user=request.user,
                    is_active=True
                )
                session.revoke()
            except UserSession.DoesNotExist:
                pass  # Session already revoked or doesn't exist
        
        return Response({
            'message': 'Logged out successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return Response({
            'message': 'Logout failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)