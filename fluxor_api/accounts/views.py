from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserUpdateSerializer, PasswordChangeSerializer, LoginHistorySerializer,
    UserSettingsSerializer, KYCUploadSerializer, NotificationSerializer
)
from .models import User, Notification

class UserRegistrationView(APIView):
    """
    Register a new user account.
    
    This endpoint allows users to create a new account with email, password, and basic information.
    The password must be at least 8 characters and pass Django's password validation.
    """
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "email": "user@example.com",
                        "full_name": "John Doe",
                        "message": "User registered successfully"
                    }
                }
            ),
            400: "Bad Request - Validation errors"
        },
        operation_description="Register a new user account with email and password"
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens for the new user
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            return Response({
                'access': access_token,
                'refresh': refresh_token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'role': user.role,
                    'is_active': user.is_active,
                    'email_verified': user.email_verified,
                    'phone_number': user.phone_number,
                    'avatar': user.avatar,
                    'date_joined': user.date_joined,
                    'last_login': user.last_login
                },
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """
    Authenticate user and return access token.
    
    This endpoint authenticates users with email and password, returning a JWT access token
    for subsequent API requests.
    """
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "full_name": "John Doe"
                        }
                    }
                }
            ),
            401: "Invalid credentials"
        },
        operation_description="Authenticate user and return JWT tokens"
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user:
                login(request, user)
                
                # Generate real JWT tokens
                from rest_framework_simplejwt.tokens import RefreshToken
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                
                return Response({
                    'access': access_token,
                    'refresh': refresh_token,
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'full_name': user.full_name,
                        'role': user.role,
                        'is_active': user.is_active,
                        'email_verified': user.email_verified,
                        'phone_number': user.phone_number,
                        'avatar': user.avatar,
                        'date_joined': user.date_joined,
                        'last_login': user.last_login
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    """
    Get and update user profile information.
    
    This endpoint allows authenticated users to view and update their profile information.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: UserProfileSerializer,
            401: "Authentication required"
        },
        operation_description="Get current user's profile information"
    )
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={
            200: openapi.Response(
                description="Profile updated successfully",
                examples={
                    "application/json": {
                        "message": "Profile updated successfully",
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "full_name": "John Doe Updated",
                            "phone_number": "+1234567890"
                        }
                    }
                }
            ),
            400: "Bad Request - Validation errors"
        },
        operation_description="Update current user's profile information"
    )
    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': UserProfileSerializer(request.user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    """
    Change user password.
    
    This endpoint allows authenticated users to change their password.
    The new password must pass Django's password validation.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=PasswordChangeSerializer,
        responses={
            200: openapi.Response(
                description="Password changed successfully",
                examples={
                    "application/json": {
                        "message": "Password changed successfully"
                    }
                }
            ),
            400: "Bad Request - Invalid current password or validation errors"
        },
        operation_description="Change current user's password"
    )
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']
            
            if not request.user.check_password(current_password):
                return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            
            request.user.set_password(new_password)
            request.user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginHistoryView(generics.ListAPIView):
    """
    Get user's login history.
    
    This endpoint returns a paginated list of the user's login attempts and sessions.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoginHistorySerializer
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
                default=1
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER,
                default=20
            )
        ],
        responses={
            200: openapi.Response(
                description="Login history retrieved successfully",
                examples={
                    "application/json": {
                        "count": 25,
                        "next": "http://localhost:8000/api/accounts/login-history/?page=2",
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "ip_address": "192.168.1.1",
                                "user_agent": "Mozilla/5.0...",
                                "timestamp": "2024-01-01T12:00:00Z",
                                "success": True
                            }
                        ]
                    }
                }
            )
        },
        operation_description="Get paginated login history for current user"
    )
    def get(self, request, *args, **kwargs):
        # Mock data for demonstration
        mock_history = [
            {
                'id': 1,
                'user': request.user.id,
                'ip_address': '192.168.1.1',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'timestamp': timezone.now(),
                'success': True
            },
            {
                'id': 2,
                'user': request.user.id,
                'ip_address': '192.168.1.2',
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'timestamp': timezone.now() - timezone.timedelta(hours=2),
                'success': True
            }
        ]
        
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        
        start = (page - 1) * page_size
        end = start + page_size
        
        return Response({
            'count': len(mock_history),
            'next': f"http://localhost:8000/api/accounts/login-history/?page={page + 1}" if end < len(mock_history) else None,
            'previous': f"http://localhost:8000/api/accounts/login-history/?page={page - 1}" if page > 1 else None,
            'results': mock_history[start:end]
        })

class UserSettingsView(APIView):
    """
    Get and update user notification settings.
    
    This endpoint allows users to manage their notification preferences.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: UserSettingsSerializer,
            401: "Authentication required"
        },
        operation_description="Get current user's notification settings"
    )
    def get(self, request):
        # Mock settings for demonstration
        settings = {
            'email_notifications': True,
            'trade_alerts': True,
            'price_alerts': False
        }
        serializer = UserSettingsSerializer(settings)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=UserSettingsSerializer,
        responses={
            200: openapi.Response(
                description="Settings updated successfully",
                examples={
                    "application/json": {
                        "message": "Settings updated successfully",
                        "settings": {
                            "email_notifications": True,
                            "trade_alerts": True,
                            "price_alerts": False
                        }
                    }
                }
            )
        },
        operation_description="Update current user's notification settings"
    )
    def put(self, request):
        serializer = UserSettingsSerializer(data=request.data)
        if serializer.is_valid():
            # In a real implementation, save settings to database
            return Response({
                'message': 'Settings updated successfully',
                'settings': serializer.validated_data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KYCUploadView(APIView):
    """
    Upload KYC documents for verification.
    
    This endpoint allows users to upload identity and address verification documents.
    Supported file types: PDF, JPG, PNG. Maximum file size: 10MB.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=KYCUploadSerializer,
        responses={
            200: openapi.Response(
                description="KYC documents uploaded successfully",
                examples={
                    "application/json": {
                        "message": "KYC documents uploaded successfully",
                        "verification_status": "pending",
                        "estimated_verification_time": "2-3 business days"
                    }
                }
            ),
            400: "Bad Request - Invalid files or validation errors"
        },
        operation_description="Upload KYC verification documents"
    )
    def post(self, request):
        serializer = KYCUploadSerializer(data=request.data)
        if serializer.is_valid():
            # In a real implementation, save files and trigger verification process
            return Response({
                'message': 'KYC documents uploaded successfully',
                'verification_status': 'pending',
                'estimated_verification_time': '2-3 business days'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@swagger_auto_schema(
    responses={
        200: openapi.Response(
            description="Logout successful",
            examples={
                "application/json": {
                    "message": "Logged out successfully"
                }
            }
        )
    },
    operation_description="Logout current user and invalidate session"
)
def logout_view(request):
    """
    Logout current user.
    
    This endpoint logs out the current user and invalidates their session.
    """
    logout(request)
    return Response({'message': 'Logged out successfully'})


class NotificationListView(generics.ListAPIView):
    """List user notifications"""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-sent_at')


class NotificationDetailView(generics.RetrieveAPIView):
    """Get notification details"""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationMarkReadView(generics.UpdateAPIView):
    """Mark notification as read"""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def put(self, request, pk):
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'is_read': True})


class NotificationMarkAllReadView(APIView):
    """Mark all notifications as read"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        updated_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
        
        return Response({'updated_count': updated_count}) 