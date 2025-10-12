from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom User model with additional fields for cryptocurrency trading platform"""
    
    # Basic Information
    firebase_uid = models.CharField(max_length=128, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Verification Status
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('under_review', 'Under Review'),
        ],
        default='pending'
    )
    
    # ID Verification (deprecated - use VerificationDocument model instead)
    id_front_image = models.URLField(blank=True, null=True)
    id_back_image = models.URLField(blank=True, null=True)
    passport_image = models.URLField(blank=True, null=True)
    verification_notes = models.TextField(blank=True, null=True)
    
    # Trading Information
    trading_level = models.CharField(
        max_length=20,
        choices=[
            ('basic', 'Basic'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('professional', 'Professional'),
        ],
        default='basic'
    )
    
    # Account Status
    account_status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('suspended', 'Suspended'),
            ('restricted', 'Restricted'),
            ('closed', 'Closed'),
        ],
        default='active'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    verification_submitted_at = models.DateTimeField(null=True, blank=True)
    verification_approved_at = models.DateTimeField(null=True, blank=True)
    
    # KYC/AML Information
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    # Security Settings
    two_factor_enabled = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.email} ({self.get_full_name() or self.username})"
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else None
    
    def is_fully_verified(self):
        """Check if user has completed all verification requirements"""
        return (
            self.is_verified and 
            self.verification_status == 'approved' and
            (self.id_front_image or self.passport_image)
        )
    
    def can_trade(self):
        """Check if user can perform trading operations"""
        return (
            self.is_active and
            self.account_status == 'active' and
            self.is_fully_verified()
        )


class UserSession(models.Model):
    """Track user sessions and tokens"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    access_token = models.TextField()
    refresh_token = models.TextField()
    firebase_token = models.TextField(blank=True, null=True)
    
    # Session Information
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    device_info = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    last_used_at = models.DateTimeField(auto_now=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_sessions'
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Session for {self.user.email} - {self.created_at}"
    
    def is_expired(self):
        """Check if session has expired"""
        return timezone.now() > self.expires_at
    
    def revoke(self):
        """Revoke the session"""
        self.is_active = False
        self.revoked_at = timezone.now()
        self.save()


class VerificationDocument(models.Model):
    """Store verification document information"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_documents')
    document_type = models.CharField(
        max_length=20,
        choices=[
            ('id_front', 'ID Card Front'),
            ('id_back', 'ID Card Back'),
            ('passport', 'Passport'),
            ('utility_bill', 'Utility Bill'),
            ('bank_statement', 'Bank Statement'),
        ]
    )
    
    # Document Information
    file = models.FileField(upload_to='verification_documents/%Y/%m/%d/', null=True, blank=True)
    file_url = models.URLField(blank=True, null=True)  # For backward compatibility
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    mime_type = models.CharField(max_length=100)
    
    # Verification Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    
    # Review Information
    reviewed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviewed_documents'
    )
    review_notes = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'verification_documents'
        verbose_name = 'Verification Document'
        verbose_name_plural = 'Verification Documents'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.get_document_type_display()}"