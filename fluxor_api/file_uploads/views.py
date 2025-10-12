from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from .models import KYCUpload
from .serializers import KYCUploadSerializer, KYCUploadCreateSerializer, KYCUploadListSerializer
import logging
import firebase_admin
from firebase_admin import auth as firebase_auth

User = get_user_model()
logger = logging.getLogger(__name__)


class FirebaseAuthentication(permissions.BasePermission):
    """Custom permission class for Firebase token authentication"""
    
    def has_permission(self, request, view):
        """Check if the request has a valid Firebase token"""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return False
        
        token = auth_header.split(' ')[1]
        
        try:
            # Verify Firebase token
            decoded_token = firebase_auth.verify_id_token(token)
            firebase_uid = decoded_token.get('uid')
            
            if not firebase_uid:
                return False
            
            # Try to get or create user
            try:
                user = User.objects.get(firebase_uid=firebase_uid)
            except User.DoesNotExist:
                # Create a temporary user for uploads (will be properly created during registration)
                user = User.objects.create(
                    firebase_uid=firebase_uid,
                    email=decoded_token.get('email', ''),
                    username=firebase_uid,
                    is_active=False  # Will be activated during registration
                )
            
            request.user = user
            return True
            
        except Exception as e:
            logger.error(f"Firebase authentication error: {str(e)}")
            return False


class KYCUploadCreateView(generics.CreateAPIView):
    """View for uploading KYC documents"""
    
    queryset = KYCUpload.objects.all()
    serializer_class = KYCUploadCreateSerializer
    permission_classes = [FirebaseAuthentication]
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_create(self, serializer):
        """Create KYC upload with user and request info"""
        # Get client IP and user agent
        ip_address = self.get_client_ip()
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        
        # Check if user already has this document type
        document_type = serializer.validated_data['document_type']
        existing_upload = KYCUpload.objects.filter(
            user=self.request.user,
            document_type=document_type
        ).first()
        
        if existing_upload:
            # Delete the old file and record
            existing_upload.delete()
        
        # Create new upload
        serializer.save(
            user=self.request.user,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
    
    def create(self, request, *args, **kwargs):
        """Handle file upload"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            with transaction.atomic():
                kyc_upload = serializer.save(
                    user=request.user,
                    ip_address=self.get_client_ip(),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                # Return the created upload data
                response_serializer = KYCUploadSerializer(kyc_upload)
                
                return Response({
                    'message': 'File uploaded successfully',
                    'upload': response_serializer.data
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            logger.error(f"KYC upload error: {str(e)}")
            return Response({
                'message': 'Upload failed',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class KYCUploadListView(generics.ListAPIView):
    """View for listing user's KYC uploads"""
    
    serializer_class = KYCUploadListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get user's KYC uploads"""
        return KYCUpload.objects.filter(user=self.request.user)


class KYCUploadDetailView(generics.RetrieveDestroyAPIView):
    """View for retrieving and deleting specific KYC uploads"""
    
    serializer_class = KYCUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get user's KYC uploads"""
        return KYCUpload.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Delete KYC upload"""
        try:
            instance = self.get_object()
            instance.delete()
            return Response({
                'message': 'KYC document deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"KYC delete error: {str(e)}")
            return Response({
                'message': 'Delete failed',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def kyc_upload_status(request):
    """Get user's KYC upload status"""
    try:
        uploads = KYCUpload.objects.filter(user=request.user)
        
        # Group by document type
        status_data = {}
        for upload in uploads:
            status_data[upload.document_type] = {
                'uploaded': True,
                'status': upload.status,
                'uploaded_at': upload.uploaded_at,
                'verified_at': upload.verified_at,
                'verification_notes': upload.verification_notes,
                'file_url': upload.get_file_url(),
            }
        
        # Add missing document types
        required_types = ['id_front', 'id_back', 'passport']
        for doc_type in required_types:
            if doc_type not in status_data:
                status_data[doc_type] = {
                    'uploaded': False,
                    'status': None,
                    'uploaded_at': None,
                    'verified_at': None,
                    'verification_notes': None,
                    'file_url': None,
                }
        
        return Response({
            'kyc_status': status_data,
            'total_uploads': uploads.count(),
            'verified_uploads': uploads.filter(status='verified').count(),
        })
        
    except Exception as e:
        logger.error(f"KYC status error: {str(e)}")
        return Response({
            'message': 'Failed to get KYC status',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bulk_kyc_upload(request):
    """Upload multiple KYC documents at once"""
    try:
        uploaded_files = []
        errors = []
        
        # Get files from request
        files = request.FILES
        document_types = request.data.getlist('document_types')
        
        if len(files) != len(document_types):
            return Response({
                'message': 'Number of files must match number of document types',
                'error': 'Mismatch between files and document types'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            for i, (file_key, file_obj) in enumerate(files.items()):
                try:
                    document_type = document_types[i]
                    
                    # Check if user already has this document type
                    existing_upload = KYCUpload.objects.filter(
                        user=request.user,
                        document_type=document_type
                    ).first()
                    
                    if existing_upload:
                        existing_upload.delete()
                    
                    # Create new upload
                    kyc_upload = KYCUpload.objects.create(
                        user=request.user,
                        document_type=document_type,
                        file=file_obj,
                        original_filename=file_obj.name,
                        file_size=file_obj.size,
                        mime_type=file_obj.content_type,
                        ip_address=request.META.get('REMOTE_ADDR'),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                    
                    uploaded_files.append(KYCUploadSerializer(kyc_upload).data)
                    
                except Exception as e:
                    errors.append({
                        'file': file_key,
                        'error': str(e)
                    })
        
        return Response({
            'message': f'Successfully uploaded {len(uploaded_files)} files',
            'uploads': uploaded_files,
            'errors': errors
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Bulk KYC upload error: {str(e)}")
        return Response({
            'message': 'Bulk upload failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)