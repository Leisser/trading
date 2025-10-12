from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserSession, VerificationDocument
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials
import os


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name', 'password', 
            'confirm_password', 'phone_number', 'date_of_birth', 'country',
            'address', 'city', 'postal_code'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': False},
        }
    
    def validate(self, attrs):
        """Validate registration data"""
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("User with this email already exists")
        
        return attrs
    
    def create(self, validated_data):
        """Create new user"""
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        
        # Generate username from email if not provided
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email']
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        
        return user


class FirebaseUserRegistrationSerializer(serializers.Serializer):
    """Serializer for Firebase user registration with ID verification"""
    
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    firebase_uid = serializers.CharField(max_length=128)
    id_images = serializers.DictField(required=False, allow_empty=True)
    
    def validate_firebase_uid(self, value):
        """Validate Firebase UID"""
        if User.objects.filter(firebase_uid=value).exists():
            raise serializers.ValidationError("User with this Firebase UID already exists")
        return value
    
    def validate_email(self, value):
        """Validate email"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value
    
    def create(self, validated_data):
        """Create user from Firebase data"""
        id_images = validated_data.pop('id_images', {})
        
        # Create user
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['name'],
            firebase_uid=validated_data['firebase_uid'],
            is_active=True,
            verification_submitted_at=timezone.now()
        )
        
        # Store ID images
        if id_images.get('front'):
            user.id_front_image = id_images['front']
        if id_images.get('back'):
            user.id_back_image = id_images['back']
        if id_images.get('passport'):
            user.passport_image = id_images['passport']
        
        user.save()
        
        return user


class TokenConversionSerializer(serializers.Serializer):
    """Serializer for converting Firebase token to backend tokens"""
    
    token = serializers.CharField()
    
    def validate_token(self, value):
        """Validate Firebase token and get user info"""
        try:
            # Use the firebase_auth_service which is already properly initialized
            from accounts.firebase_auth import firebase_auth_service
            
            # Verify the token using our service
            firebase_data = firebase_auth_service.verify_firebase_token(value)
            
            if not firebase_data:
                raise serializers.ValidationError("Your session has expired. Please sign in again.")
                
            return firebase_data
            
        except serializers.ValidationError:
            raise
        except Exception as e:
            # Log the technical error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Firebase token validation error: {str(e)}")
            
            # Return user-friendly message
            error_msg = str(e).lower()
            if 'expired' in error_msg:
                raise serializers.ValidationError("Your session has expired. Please sign in again.")
            elif 'revoked' in error_msg:
                raise serializers.ValidationError("Your session has been revoked. Please sign in again.")
            else:
                raise serializers.ValidationError("Authentication failed. Please sign in again.")
    
    def create(self, validated_data):
        """Get or create user and return session tokens"""
        firebase_data = validated_data['token']
        email = firebase_data.get('email')
        firebase_uid = firebase_data.get('uid')
        
        if not email or not firebase_uid:
            raise serializers.ValidationError("Invalid Firebase data: missing email or uid")
        
        # Check if user exists by email (primary) or Firebase UID (secondary)
        user = None
        
        # First, try to find by email
        try:
            user = User.objects.get(email=email)
            # Update Firebase UID if not set or different
            if user.firebase_uid != firebase_uid:
                user.firebase_uid = firebase_uid
                user.save(update_fields=['firebase_uid'])
        except User.DoesNotExist:
            # Try by Firebase UID
            try:
                user = User.objects.get(firebase_uid=firebase_uid)
            except User.DoesNotExist:
                # User doesn't exist - create new user
                from accounts.firebase_auth import firebase_auth_service
                user = firebase_auth_service.get_or_create_user_from_firebase(firebase_data)
                
                if not user:
                    raise serializers.ValidationError("Failed to create account. Please try again.")
        
        # Create JWT tokens
        from rest_framework_simplejwt.tokens import RefreshToken
        from django.utils import timezone
        from datetime import timedelta
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Create session for tracking
        session = UserSession.objects.create(
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
            firebase_token=validated_data['token'],
            expires_at=timezone.now() + timedelta(hours=24),
            ip_address=self.context.get('request').META.get('REMOTE_ADDR'),
            user_agent=self.context.get('request').META.get('HTTP_USER_AGENT', ''),
        )
        
        # Update user's last login
        user.last_login_at = timezone.now()
        user.save()
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': UserSerializer(user).data
        }


class RefreshTokenSerializer(serializers.Serializer):
    """Serializer for refreshing access token"""
    
    refresh_token = serializers.CharField()
    
    def validate_refresh_token(self, value):
        """Validate refresh token"""
        try:
            session = UserSession.objects.get(
                refresh_token=value,
                is_active=True,
                revoked_at__isnull=True
            )
            
            if session.is_expired():
                raise serializers.ValidationError("Refresh token has expired")
            
            return session
            
        except UserSession.DoesNotExist:
            raise serializers.ValidationError("Invalid refresh token")
    
    def create(self, validated_data):
        """Generate new access token"""
        from rest_framework_simplejwt.tokens import RefreshToken
        
        session = validated_data['refresh_token']
        
        # Generate new JWT tokens
        refresh = RefreshToken.for_user(session.user)
        new_access_token = str(refresh.access_token)
        new_refresh_token = str(refresh)
        
        session.access_token = new_access_token
        session.refresh_token = new_refresh_token
        session.save()
        
        return {
            'access_token': new_access_token,
            'refresh_token': new_refresh_token
        }


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data"""
    
    full_name = serializers.SerializerMethodField()
    is_fully_verified = serializers.SerializerMethodField()
    can_trade = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'phone_number', 'date_of_birth', 'country', 'address', 'city', 'postal_code',
            'is_verified', 'verification_status', 'trading_level', 'account_status',
            'is_fully_verified', 'can_trade', 'two_factor_enabled',
            'email_notifications', 'sms_notifications', 'is_superuser', 'is_staff',
            'created_at', 'last_login_at', 'verification_submitted_at',
            'verification_approved_at'
        ]
        read_only_fields = [
            'id', 'is_verified', 'verification_status', 'trading_level',
            'account_status', 'created_at', 'last_login_at',
            'verification_submitted_at', 'verification_approved_at'
        ]
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_is_fully_verified(self, obj):
        return obj.is_fully_verified()
    
    def get_can_trade(self, obj):
        return obj.can_trade()


class UserSessionSerializer(serializers.ModelSerializer):
    """Serializer for user session data"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserSession
        fields = [
            'id', 'user', 'ip_address', 'user_agent', 'device_info',
            'created_at', 'expires_at', 'last_used_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'expires_at', 'last_used_at']


class VerificationDocumentSerializer(serializers.ModelSerializer):
    """Serializer for verification documents"""
    
    class Meta:
        model = VerificationDocument
        fields = [
            'id', 'document_type', 'file_url', 'file_name', 'file_size',
            'mime_type', 'status', 'review_notes', 'uploaded_at',
            'reviewed_at', 'reviewed_by'
        ]
        read_only_fields = [
            'id', 'status', 'review_notes', 'uploaded_at', 'reviewed_at',
            'reviewed_by'
        ]