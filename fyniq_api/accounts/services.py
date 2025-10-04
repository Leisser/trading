from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import User, AuditLog, Notification

class UserManagementService:
    """Service for user management operations"""
    
    @staticmethod
    def ban_user(user, admin_user, reason):
        """Ban a user"""
        user.is_banned = True
        user.ban_reason = reason
        user.banned_at = timezone.now()
        user.banned_by = admin_user
        user.is_active = False
        user.save()
        
        # Create audit log
        AuditLog.objects.create(
            user=user,
            admin_user=admin_user,
            action='user_banned',
            details={
                'reason': reason,
                'banned_at': user.banned_at.isoformat()
            },
            ip_address=getattr(admin_user, 'last_ip', None)
        )
        
        # Send notification
        NotificationService.create_notification(
            user=user,
            notification_type='email',
            title='Account Banned',
            message=f'Your account has been banned. Reason: {reason}',
            priority='urgent'
        )
        
        return user
    
    @staticmethod
    def unban_user(user, admin_user, reason=None):
        """Unban a user"""
        user.is_banned = False
        user.ban_reason = ''
        user.banned_at = None
        user.banned_by = None
        user.is_active = True
        user.save()
        
        # Create audit log
        AuditLog.objects.create(
            user=user,
            admin_user=admin_user,
            action='user_unbanned',
            details={
                'reason': reason or 'No reason provided',
                'unbanned_at': timezone.now().isoformat()
            },
            ip_address=getattr(admin_user, 'last_ip', None)
        )
        
        # Send notification
        NotificationService.create_notification(
            user=user,
            notification_type='email',
            title='Account Unbanned',
            message='Your account has been unbanned. You can now log in again.',
            priority='high'
        )
        
        return user
    
    @staticmethod
    def freeze_user(user, admin_user, reason):
        """Freeze a user account"""
        user.is_frozen = True
        user.freeze_reason = reason
        user.frozen_at = timezone.now()
        user.frozen_by = admin_user
        user.save()
        
        # Create audit log
        AuditLog.objects.create(
            user=user,
            admin_user=admin_user,
            action='user_frozen',
            details={
                'reason': reason,
                'frozen_at': user.frozen_at.isoformat()
            },
            ip_address=getattr(admin_user, 'last_ip', None)
        )
        
        # Send notification
        NotificationService.create_notification(
            user=user,
            notification_type='email',
            title='Account Frozen',
            message=f'Your account has been frozen. Reason: {reason}',
            priority='high'
        )
        
        return user
    
    @staticmethod
    def unfreeze_user(user, admin_user, reason=None):
        """Unfreeze a user account"""
        user.is_frozen = False
        user.freeze_reason = ''
        user.frozen_at = None
        user.frozen_by = None
        user.save()
        
        # Create audit log
        AuditLog.objects.create(
            user=user,
            admin_user=admin_user,
            action='user_unfrozen',
            details={
                'reason': reason or 'No reason provided',
                'unfrozen_at': timezone.now().isoformat()
            },
            ip_address=getattr(admin_user, 'last_ip', None)
        )
        
        # Send notification
        NotificationService.create_notification(
            user=user,
            notification_type='email',
            title='Account Unfrozen',
            message='Your account has been unfrozen. You can now use all features.',
            priority='high'
        )
        
        return user


class AuditLogService:
    """Service for audit logging"""
    
    @staticmethod
    def log_action(user, action, details=None, admin_user=None, ip_address=None, user_agent=None):
        """Log an action to the audit log"""
        return AuditLog.objects.create(
            user=user,
            admin_user=admin_user,
            action=action,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    @staticmethod
    def log_login_success(user, ip_address, user_agent):
        """Log successful login"""
        return AuditLogService.log_action(
            user=user,
            action='login_success',
            details={'ip_address': ip_address},
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    @staticmethod
    def log_login_failed(email, ip_address, user_agent, reason='Invalid credentials'):
        """Log failed login attempt"""
        return AuditLogService.log_action(
            user=None,
            action='login_failed',
            details={
                'email': email,
                'ip_address': ip_address,
                'reason': reason
            },
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    @staticmethod
    def log_security_alert(user, alert_type, details):
        """Log security alert"""
        return AuditLogService.log_action(
            user=user,
            action='security_alert',
            details={
                'alert_type': alert_type,
                **details
            }
        )


class NotificationService:
    """Service for notifications"""
    
    @staticmethod
    def create_notification(user, notification_type, title, message, priority='medium'):
        """Create a notification"""
        return Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            priority=priority
        )
    
    @staticmethod
    def send_email_notification(user, subject, message):
        """Send email notification"""
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            # Create notification record
            NotificationService.create_notification(
                user=user,
                notification_type='email',
                title=subject,
                message=message,
                priority='medium'
            )
            
            return True
        except Exception as e:
            print(f"Failed to send email notification: {str(e)}")
            return False
    
    @staticmethod
    def send_notification(notification):
        """Simulate sending a single notification."""
        # In a real application, this would integrate with email, SMS, or push notification services.
        print(f"Sending notification to {notification.user.email}: {notification.title} - {notification.message}")
        return True

    @staticmethod
    def send_batch_notifications(notifications):
        """Simulate sending a batch of notifications."""
        results = []
        for notification in notifications:
            results.append(NotificationService.send_notification(notification))
        return results

    @staticmethod
    def mark_as_read(notification_id, user):
        """Mark notification as read"""
        try:
            notification = Notification.objects.get(id=notification_id, user=user)
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
            return True
        except Notification.DoesNotExist:
            return False 