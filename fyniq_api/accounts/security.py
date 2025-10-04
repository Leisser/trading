"""
Advanced Security System for Fluxor Trading API
Includes 2FA, threat detection, and security monitoring
"""

import pyotp
import qrcode
import io
import base64
import hashlib
import secrets
import time
import geoip2.database
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class TwoFactorAuthService:
    """Two-Factor Authentication service"""
    
    @staticmethod
    def generate_secret():
        """Generate a new TOTP secret"""
        return pyotp.random_base32()
    
    @staticmethod
    def get_qr_code(user, secret):
        """Generate QR code for 2FA setup"""
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user.email,
            issuer_name="Fluxor Trading"
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    @staticmethod
    def verify_token(secret, token):
        """Verify TOTP token"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)  # Allow 30 seconds window
    
    @staticmethod
    def get_backup_codes():
        """Generate backup codes for 2FA"""
        codes = []
        for _ in range(10):
            code = secrets.token_hex(4)  # 8-character hex codes
            codes.append(code)
        return codes


class SecurityMonitoringService:
    """Security monitoring and threat detection"""
    
    def __init__(self):
        self.max_failed_attempts = 5
        self.lockout_duration = 900  # 15 minutes
        self.suspicious_activity_threshold = 10
    
    def log_login_attempt(self, user, ip_address, user_agent, success=True):
        """Log login attempt for security monitoring"""
        from accounts.models import LoginHistory, AuditLog
        
        # Create login history record
        LoginHistory.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success
        )
        
        # Create audit log
        AuditLog.objects.create(
            user=user,
            action='login_success' if success else 'login_failed',
            details={
                'ip_address': ip_address,
                'user_agent': user_agent,
                'timestamp': timezone.now().isoformat()
            },
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        if not success:
            self._check_brute_force(ip_address, user.email if user else None)
    
    def _check_brute_force(self, ip_address, email=None):
        """Check for brute force attacks"""
        cache_key_ip = f"failed_attempts:{ip_address}"
        cache_key_email = f"failed_attempts:email:{email}" if email else None
        
        # Track by IP
        ip_attempts = cache.get(cache_key_ip, 0) + 1
        cache.set(cache_key_ip, ip_attempts, self.lockout_duration)
        
        # Track by email if provided
        if cache_key_email:
            email_attempts = cache.get(cache_key_email, 0) + 1
            cache.set(cache_key_email, email_attempts, self.lockout_duration)
        
        if ip_attempts >= self.max_failed_attempts:
            self._trigger_security_alert('brute_force_ip', {
                'ip_address': ip_address,
                'attempts': ip_attempts
            })
        
        if email and cache.get(cache_key_email, 0) >= self.max_failed_attempts:
            self._trigger_security_alert('brute_force_email', {
                'email': email,
                'attempts': cache.get(cache_key_email, 0)
            })
    
    def is_ip_blocked(self, ip_address):
        """Check if IP is temporarily blocked"""
        attempts = cache.get(f"failed_attempts:{ip_address}", 0)
        return attempts >= self.max_failed_attempts
    
    def is_email_blocked(self, email):
        """Check if email is temporarily blocked"""
        attempts = cache.get(f"failed_attempts:email:{email}", 0)
        return attempts >= self.max_failed_attempts
    
    def clear_failed_attempts(self, ip_address, email=None):
        """Clear failed attempts after successful login"""
        cache.delete(f"failed_attempts:{ip_address}")
        if email:
            cache.delete(f"failed_attempts:email:{email}")
    
    def detect_unusual_activity(self, user, ip_address, user_agent):
        """Detect unusual activity patterns"""
        from accounts.models import LoginHistory
        
        # Check for new location
        if self._is_new_location(user, ip_address):
            self._trigger_security_alert('new_location', {
                'user': user.email,
                'ip_address': ip_address,
                'location': self._get_location(ip_address)
            })
        
        # Check for new device
        if self._is_new_device(user, user_agent):
            self._trigger_security_alert('new_device', {
                'user': user.email,
                'user_agent': user_agent
            })
        
        # Check for rapid logins
        recent_logins = LoginHistory.objects.filter(
            user=user,
            login_time__gte=timezone.now() - timedelta(minutes=5),
            success=True
        ).count()
        
        if recent_logins > 3:
            self._trigger_security_alert('rapid_logins', {
                'user': user.email,
                'recent_logins': recent_logins
            })
    
    def _is_new_location(self, user, ip_address):
        """Check if login is from a new geographic location"""
        from accounts.models import LoginHistory
        
        # Get recent successful logins
        recent_logins = LoginHistory.objects.filter(
            user=user,
            success=True,
            login_time__gte=timezone.now() - timedelta(days=30)
        ).values_list('ip_address', flat=True).distinct()
        
        # Simple check - in production, you'd use more sophisticated geo-IP
        return ip_address not in recent_logins
    
    def _is_new_device(self, user, user_agent):
        """Check if login is from a new device"""
        from accounts.models import LoginHistory
        
        # Get recent user agents
        recent_agents = LoginHistory.objects.filter(
            user=user,
            success=True,
            login_time__gte=timezone.now() - timedelta(days=30)
        ).values_list('user_agent', flat=True).distinct()
        
        return user_agent not in recent_agents
    
    def _get_location(self, ip_address):
        """Get location from IP address"""
        try:
            # This would require a GeoIP database
            # For now, return placeholder
            return {"country": "Unknown", "city": "Unknown"}
        except:
            return {"country": "Unknown", "city": "Unknown"}
    
    def _trigger_security_alert(self, alert_type, details):
        """Trigger security alert"""
        from accounts.models import AuditLog
        
        logger.warning(f"Security alert: {alert_type} - {details}")
        
        # Create audit log for security event
        AuditLog.objects.create(
            action='security_alert',
            details={
                'alert_type': alert_type,
                'details': details,
                'timestamp': timezone.now().isoformat()
            }
        )
        
        # Here you could also send notifications, etc.


class EncryptionService:
    """Encryption service for sensitive data"""
    
    def __init__(self):
        self.key = settings.CRYPTO_ENCRYPTION_KEY.encode() if hasattr(settings, 'CRYPTO_ENCRYPTION_KEY') else Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data):
        """Encrypt sensitive data"""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data).decode()
    
    def decrypt(self, encrypted_data):
        """Decrypt sensitive data"""
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        return self.cipher.decrypt(encrypted_data).decode()


class APIKeyService:
    """API Key management service"""
    
    @staticmethod
    def generate_api_key():
        """Generate new API key"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_api_key(api_key):
        """Hash API key for storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    @staticmethod
    def verify_api_key(api_key, hashed_key):
        """Verify API key against hash"""
        return hashlib.sha256(api_key.encode()).hexdigest() == hashed_key


# API Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_2fa(request):
    """Setup 2FA for user"""
    user = request.user
    
    if user.profile.two_factor_enabled:
        return Response({
            'error': '2FA is already enabled'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate secret
    secret = TwoFactorAuthService.generate_secret()
    
    # Store secret temporarily (user needs to verify it first)
    cache.set(f"2fa_setup:{user.id}", secret, 300)  # 5 minutes
    
    # Generate QR code
    qr_code = TwoFactorAuthService.get_qr_code(user, secret)
    
    return Response({
        'qr_code': qr_code,
        'secret': secret,  # Also return secret for manual entry
        'message': 'Scan QR code with your authenticator app'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_2fa_setup(request):
    """Verify 2FA setup with token"""
    user = request.user
    token = request.data.get('token')
    
    if not token:
        return Response({
            'error': 'Token is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Get temporary secret
    secret = cache.get(f"2fa_setup:{user.id}")
    if not secret:
        return Response({
            'error': '2FA setup expired. Please start over.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify token
    if not TwoFactorAuthService.verify_token(secret, token):
        return Response({
            'error': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Save secret and enable 2FA
    encryption_service = EncryptionService()
    encrypted_secret = encryption_service.encrypt(secret)
    
    user.profile.two_factor_secret = encrypted_secret
    user.profile.two_factor_enabled = True
    user.profile.save()
    
    # Generate backup codes
    backup_codes = TwoFactorAuthService.get_backup_codes()
    encrypted_codes = [encryption_service.encrypt(code) for code in backup_codes]
    
    # Store backup codes (you'd need a model for this)
    # For now, just return them to the user
    
    # Clear temporary secret
    cache.delete(f"2fa_setup:{user.id}")
    
    return Response({
        'message': '2FA enabled successfully',
        'backup_codes': backup_codes  # In production, show these only once
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disable_2fa(request):
    """Disable 2FA for user"""
    user = request.user
    password = request.data.get('password')
    
    if not user.check_password(password):
        return Response({
            'error': 'Invalid password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user.profile.two_factor_enabled = False
    user.profile.two_factor_secret = ''
    user.profile.save()
    
    return Response({
        'message': '2FA disabled successfully'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def security_overview(request):
    """Get security overview for user"""
    user = request.user
    from accounts.models import LoginHistory
    
    # Get recent login history
    recent_logins = LoginHistory.objects.filter(
        user=user,
        login_time__gte=timezone.now() - timedelta(days=30)
    ).order_by('-login_time')[:10]
    
    login_data = []
    for login in recent_logins:
        login_data.append({
            'ip_address': login.ip_address,
            'location': 'Unknown',  # Would get from GeoIP
            'device': 'Unknown',    # Would parse from user_agent
            'time': login.login_time.isoformat(),
            'success': login.success
        })
    
    return Response({
        'two_factor_enabled': user.profile.two_factor_enabled,
        'recent_logins': login_data,
        'active_sessions': 1,  # Would track active sessions
        'security_score': 85   # Would calculate based on security features
    })