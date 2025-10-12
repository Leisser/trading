from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import os
import uuid

User = get_user_model()


def kyc_upload_path(instance, filename):
    """Generate upload path for KYC documents"""
    # Create a unique filename to prevent conflicts
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    
    # Organize by user ID and document type
    return os.path.join('kyc', str(instance.user.id), instance.document_type, filename)


class KYCUpload(models.Model):
    """Model for tracking KYC document uploads"""
    
    DOCUMENT_TYPES = [
        ('id_front', 'ID Card Front'),
        ('id_back', 'ID Card Back'),
        ('passport', 'Passport'),
        ('utility_bill', 'Utility Bill'),
        ('bank_statement', 'Bank Statement'),
        ('selfie', 'Selfie with ID'),
    ]
    
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kyc_uploads')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    
    # File Information
    file = models.FileField(upload_to=kyc_upload_path)
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    mime_type = models.CharField(max_length=100)
    
    # Upload Information
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    
    # Verification Information
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_kyc')
    verification_notes = models.TextField(blank=True, null=True)
    
    # Security Information
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'kyc_uploads'
        verbose_name = 'KYC Upload'
        verbose_name_plural = 'KYC Uploads'
        ordering = ['-uploaded_at']
        unique_together = ['user', 'document_type']
    
    def __str__(self):
        return f"{self.user.email} - {self.get_document_type_display()}"
    
    def get_file_url(self):
        """Get the URL for the uploaded file"""
        if self.file:
            return self.file.url
        return None
    
    def get_file_path(self):
        """Get the local file path"""
        if self.file:
            return self.file.path
        return None
    
    def delete_file(self):
        """Delete the physical file from storage"""
        if self.file and os.path.exists(self.file.path):
            os.remove(self.file.path)
    
    def save(self, *args, **kwargs):
        # Set file information if file is provided
        if self.file and not self.file_size:
            self.file_size = self.file.size
        if self.file and not self.mime_type:
            self.mime_type = self.file.content_type
        if self.file and not self.original_filename:
            self.original_filename = os.path.basename(self.file.name)
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Delete the physical file when the model is deleted
        self.delete_file()
        super().delete(*args, **kwargs)