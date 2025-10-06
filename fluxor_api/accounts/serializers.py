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
            # Initialize Firebase Admin SDK if not already done
            if not firebase_admin._apps:
                # Use service account key from environment or default
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
            decoded_token = firebase_auth.verify_id_token(value)
            return decoded_token
            
        except Exception as e:
            raise serializers.ValidationError(f"Invalid Firebase token: {str(e)}")
    
    def create(self, validated_data):
        """Create or get user session and return tokens"""
        decoded_token = validated_data['token']
        firebase_uid = decoded_token['uid']
        
        try:
            # Get or create user
            user = User.objects.get(firebase_uid=firebase_uid)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found. Please register first.")
        
        # Create session
        from django.utils import timezone
        from datetime import timedelta
        
        session = UserSession.objects.create(
            user=user,
            access_token=self.generate_access_token(user),
            refresh_token=self.generate_refresh_token(user),
            firebase_token=validated_data['token'],
            expires_at=timezone.now() + timedelta(hours=24),
            ip_address=self.context.get('request').META.get('REMOTE_ADDR'),
            user_agent=self.context.get('request').META.get('HTTP_USER_AGENT', ''),
        )
        
        # Update user's last login
        user.last_login_at = timezone.now()
        user.save()
        
        return {
            'access_token': session.access_token,
            'refresh_token': session.refresh_token,
            'user': UserSerializer(user).data
        }
    
    def generate_access_token(self, user):
        """Generate access token (simplified - use JWT in production)"""
        import hashlib
        import time
        token_data = f"{user.id}:{user.email}:{time.time()}"
        return hashlib.sha256(token_data.encode()).hexdigest()
    
    def generate_refresh_token(self, user):
        """Generate refresh token (simplified - use JWT in production)"""
        import hashlib
        import time
        token_data = f"refresh:{user.id}:{user.email}:{time.time()}"
        return hashlib.sha256(token_data.encode()).hexdigest()


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
        session = validated_data['refresh_token']
        
        # Generate new access token
        new_access_token = self.generate_access_token(session.user)
        session.access_token = new_access_token
        session.save()
        
        return {
            'access_token': new_access_token,
            'refresh_token': session.refresh_token
        }
    
    def generate_access_token(self, user):
        """Generate access token (simplified - use JWT in production)"""
        import hashlib
        import time
        token_data = f"{user.id}:{user.email}:{time.time()}"
        return hashlib.sha256(token_data.encode()).hexdigest()


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
            'email_notifications', 'sms_notifications',
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