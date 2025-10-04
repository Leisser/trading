from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Notification

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with password confirmation.
    
    Example:
    {
        "email": "user@example.com",
        "full_name": "John Doe",
        "password": "securepassword123",
        "password_confirm": "securepassword123",
        "phone_number": "+1234567890"
    }
    """
    password = serializers.CharField(write_only=True, min_length=8, help_text="Password must be at least 8 characters")
    password_confirm = serializers.CharField(write_only=True, help_text="Must match the password field")
    phone_number = serializers.CharField(required=False, allow_blank=True, help_text="Optional phone number")
    
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'password_confirm', 'phone_number']
        extra_kwargs = {
            'email': {'help_text': 'Valid email address required'},
            'full_name': {'help_text': 'User\'s full name'},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Example:
    {
        "email": "user@example.com",
        "password": "securepassword123"
    }
    """
    email = serializers.EmailField(help_text="User's email address")
    password = serializers.CharField(write_only=True, help_text="User's password")

class UserSerializer(serializers.ModelSerializer):
    """
    General user serializer for API responses.
    
    Example Response:
    {
        "id": 1,
        "email": "user@example.com",
        "full_name": "John Doe",
        "phone_number": "+1234567890",
        "avatar": "https://example.com/avatar.jpg",
        "email_verified": true,
        "role": "user",
        "is_active": true,
        "date_joined": "2024-01-01T00:00:00Z",
        "last_login": "2024-01-01T12:00:00Z",
        "auth_provider": "firebase"
    }
    """
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'phone_number', 'avatar',
            'email_verified', 'role', 'is_active', 'date_joined', 
            'last_login', 'auth_provider', 'firebase_uid'
        ]
        read_only_fields = ['id', 'email', 'role', 'is_active', 'date_joined', 'last_login']

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    
    Example Response:
    {
        "id": 1,
        "email": "user@example.com",
        "full_name": "John Doe",
        "phone_number": "+1234567890",
        "date_of_birth": "1990-01-01",
        "address": "123 Main St, New York, NY 10001",
        "is_verified": true,
        "kyc_verified": false,
        "role": "user",
        "date_joined": "2024-01-01T00:00:00Z"
    }
    """
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'phone_number', 'date_of_birth',
            'address', 'is_verified', 'kyc_verified', 'role', 'date_joined'
        ]
        read_only_fields = ['id', 'email', 'is_verified', 'kyc_verified', 'role', 'date_joined']

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    
    Example:
    {
        "full_name": "John Doe Updated",
        "phone_number": "+1234567890",
        "date_of_birth": "1990-01-01",
        "address": "123 Main St, New York, NY 10001"
    }
    """
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'date_of_birth', 'address']

class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change.
    
    Example:
    {
        "current_password": "oldpassword123",
        "new_password": "newpassword123"
    }
    """
    current_password = serializers.CharField(write_only=True, help_text="Current password")
    new_password = serializers.CharField(write_only=True, min_length=8, help_text="New password (min 8 characters)")
    
    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

class LoginHistorySerializer(serializers.Serializer):
    """
    Serializer for login history.
    
    Example Response:
    {
        "id": 1,
        "user": 1,
        "ip_address": "192.168.1.1",
        "user_agent": "Mozilla/5.0...",
        "timestamp": "2024-01-01T12:00:00Z",
        "success": true
    }
    """
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(read_only=True)
    ip_address = serializers.CharField(read_only=True)
    user_agent = serializers.CharField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)
    success = serializers.BooleanField(read_only=True)

class UserSettingsSerializer(serializers.Serializer):
    """
    Serializer for user notification settings.
    
    Example:
    {
        "email_notifications": true,
        "trade_alerts": true,
        "price_alerts": false
    }
    """
    email_notifications = serializers.BooleanField(default=True, help_text="Receive email notifications")
    trade_alerts = serializers.BooleanField(default=True, help_text="Get notified when trades are executed")
    price_alerts = serializers.BooleanField(default=False, help_text="Receive alerts for significant price movements")

class KYCUploadSerializer(serializers.Serializer):
    """
    Serializer for KYC document upload.
    
    Example:
    {
        "id_document": <file>,
        "address_document": <file>,
        "selfie": <file>
    }
    """
    id_document = serializers.FileField(help_text="Government ID (Passport/Driver's License)")
    address_document = serializers.FileField(help_text="Proof of Address (Utility Bill/Bank Statement)")
    selfie = serializers.ImageField(help_text="Selfie with ID")
    
    def validate_id_document(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size must be under 10MB")
        return value
    
    def validate_address_document(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size must be under 10MB")
        return value
    
    def validate_selfie(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("File size must be under 5MB")
        return value


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'notification_type', 'title', 'message', 
            'priority', 'is_read', 'sent_at', 'read_at'
        ]
        read_only_fields = ['id', 'user', 'sent_at', 'read_at'] 