from rest_framework import serializers
from .models import KYCUpload
from django.contrib.auth import get_user_model

User = get_user_model()


class KYCUploadSerializer(serializers.ModelSerializer):
    """Serializer for KYC uploads"""
    
    file_url = serializers.SerializerMethodField()
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = KYCUpload
        fields = [
            'id',
            'document_type',
            'document_type_display',
            'file_url',
            'original_filename',
            'file_size',
            'mime_type',
            'uploaded_at',
            'status',
            'status_display',
            'verified_at',
            'verification_notes',
        ]
        read_only_fields = [
            'id',
            'file_url',
            'original_filename',
            'file_size',
            'mime_type',
            'uploaded_at',
            'status',
            'verified_at',
            'verification_notes',
        ]
    
    def get_file_url(self, obj):
        """Get the file URL"""
        return obj.get_file_url()


class KYCUploadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating KYC uploads"""
    
    class Meta:
        model = KYCUpload
        fields = [
            'document_type',
            'file',
        ]
    
    def validate_file(self, value):
        """Validate uploaded file"""
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size must be less than 10MB")
        
        # Check file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'application/pdf']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                f"File type not allowed. Allowed types: {', '.join(allowed_types)}"
            )
        
        return value
    
    def validate_document_type(self, value):
        """Validate document type"""
        allowed_types = [choice[0] for choice in KYCUpload.DOCUMENT_TYPES]
        if value not in allowed_types:
            raise serializers.ValidationError(f"Invalid document type. Allowed types: {', '.join(allowed_types)}")
        
        return value


class KYCUploadListSerializer(serializers.ModelSerializer):
    """Serializer for listing KYC uploads"""
    
    file_url = serializers.SerializerMethodField()
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = KYCUpload
        fields = [
            'id',
            'document_type',
            'document_type_display',
            'file_url',
            'original_filename',
            'file_size',
            'mime_type',
            'uploaded_at',
            'status',
            'status_display',
            'verified_at',
            'verification_notes',
        ]
    
    def get_file_url(self, obj):
        """Get the file URL"""
        return obj.get_file_url()
