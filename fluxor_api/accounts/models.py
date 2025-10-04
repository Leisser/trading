from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Fix reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='fluxor_user_set',
        related_query_name='fluxor_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='fluxor_user_set',
        related_query_name='fluxor_user',
    )
    
    # KYC fields
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    id_document = models.FileField(upload_to='kyc_documents/', blank=True)
    kyc_verified = models.BooleanField(default=False)
    kyc_verified_at = models.DateTimeField(null=True, blank=True)
    
    # Ban/Freeze fields
    is_banned = models.BooleanField(default=False)
    is_frozen = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True)
    freeze_reason = models.TextField(blank=True)
    banned_at = models.DateTimeField(null=True, blank=True)
    frozen_at = models.DateTimeField(null=True, blank=True)
    banned_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='banned_users')
    frozen_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='frozen_users')
    
    # Firebase Authentication fields
    firebase_uid = models.CharField(max_length=128, blank=True, null=True, unique=True)
    auth_provider = models.CharField(max_length=20, choices=[
        ('email', 'Email/Password'),
        ('google', 'Google'),
        ('apple', 'Apple'),
        ('firebase', 'Firebase'),
    ], default='email')
    avatar = models.URLField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.split()[0] if self.full_name else self.email
    
    def validate_password_strength(self, password):
        """Validate password strength"""
        import re
        
        # Check minimum length
        if len(password) < 8:
            return False
        
        # Check for common passwords
        common_passwords = ['password', '123456', '12345678', 'qwerty', 'abc123']
        if password.lower() in common_passwords:
            return False
        
        # Check for at least one uppercase, one lowercase, one digit
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        
        return True
    
    def record_failed_login_attempt(self):
        """Record a failed login attempt"""
        LoginHistory.objects.create(
            user=self,
            ip_address='127.0.0.1',  # This should be passed from the view
            user_agent='Unknown',
            success=False
        )
    
    def is_locked_out(self):
        """Check if user is locked out due to too many failed attempts"""
        from django.utils import timezone
        from datetime import timedelta
        
        # Check failed attempts in the last hour
        one_hour_ago = timezone.now() - timedelta(hours=1)
        failed_attempts = LoginHistory.objects.filter(
            user=self,
            success=False,
            login_time__gte=one_hour_ago
        ).count()
        
        return failed_attempts >= 5  # Lock after 5 failed attempts


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Trading preferences
    default_currency = models.CharField(max_length=3, default='USD')
    notifications_enabled = models.BooleanField(default=True)
    two_factor_enabled = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} Profile"


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    login_time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Login Histories"
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.email} - {self.login_time}"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('user_created', 'User Created'),
        ('user_updated', 'User Updated'),
        ('user_banned', 'User Banned'),
        ('user_unbanned', 'User Unbanned'),
        ('user_frozen', 'User Frozen'),
        ('user_unfrozen', 'User Unfrozen'),
        ('kyc_verified', 'KYC Verified'),
        ('kyc_rejected', 'KYC Rejected'),
        ('login_success', 'Login Success'),
        ('login_failed', 'Login Failed'),
        ('password_changed', 'Password Changed'),
        ('wallet_created', 'Wallet Created'),
        ('deposit_received', 'Deposit Received'),
        ('withdrawal_requested', 'Withdrawal Requested'),
        ('withdrawal_approved', 'Withdrawal Approved'),
        ('withdrawal_rejected', 'Withdrawal Rejected'),
        ('withdrawal_completed', 'Withdrawal Completed'),
        ('trade_executed', 'Trade Executed'),
        ('admin_action', 'Admin Action'),
        ('security_alert', 'Security Alert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs', null=True, blank=True)
    admin_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_actions')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action} - {self.user.email if self.user else 'System'} - {self.timestamp}"


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push'),
        ('in_app', 'In-App'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.email} - {self.sent_at}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        from django.utils import timezone
        
        self.is_read = True
        self.read_at = timezone.now()
        self.save() 