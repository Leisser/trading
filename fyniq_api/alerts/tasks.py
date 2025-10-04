import logging
from decimal import Decimal
from celery import shared_task
from django.utils import timezone
from django.db import transaction

logger = logging.getLogger(__name__)

@shared_task
def process_alerts():
    """Process all pending alerts"""
    try:
        from .models import Alert, TradingSignal, AlertTrigger
        
        # Process price alerts
        process_price_alerts.delay()
        
        # Process trading signals
        process_trading_signals.delay()
        
        # Process alert triggers
        process_alert_triggers.delay()
        
        # Process market alerts
        process_market_alerts.delay()
        
        return True
        
    except Exception as e:
        logger.error(f"Error in process_alerts: {str(e)}")
        raise

@shared_task
def create_price_alert(trading_pair_id, price_change_percent, current_price):
    """Create a price alert for significant price movements"""
    try:
        from .models import Alert, MarketAlert
        
        # Create market alert
        alert = MarketAlert.objects.create(
            category='high_volatility',
            severity='warning',
            title=f"Significant Price Movement: {trading_pair_id}",
            message=f"Price changed by {price_change_percent:.2f}% to ${current_price:.2f}",
            affected_pairs=[trading_pair_id],
            is_active=True,
        )
        
        # Notify subscribed users
        notify_subscribed_users.delay(alert.id)
        
        logger.info(f"Created price alert for {trading_pair_id}: {price_change_percent:.2f}% change")
        return alert.id
        
    except Exception as e:
        logger.error(f"Error creating price alert: {str(e)}")
        raise

@shared_task
def create_risk_alert(user_id, alert_type, severity, message):
    """Create a risk management alert"""
    try:
        from accounts.models import User
        from .models import Alert
        
        user = User.objects.get(id=user_id)
        
        alert = Alert.objects.create(
            user=user,
            name=f"Risk Alert: {alert_type}",
            alert_type='custom',
            priority=severity,
            message=message,
            status='active',
        )
        
        # Send immediate notification
        send_notification.delay(user.id, alert.id)
        
        logger.info(f"Created risk alert for user {user_id}: {alert_type}")
        return alert.id
        
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return None
    except Exception as e:
        logger.error(f"Error creating risk alert: {str(e)}")
        raise

@shared_task
def process_price_alerts():
    """Process price-based alerts"""
    try:
        from .models import Alert
        from market_data.models import Ticker
        
        # Get active price alerts
        price_alerts = Alert.objects.filter(
            alert_type__in=['price_above', 'price_below'],
            status='active'
        ).select_related('user')
        
        for alert in price_alerts:
            try:
                # Get current price - simplified since we don't have trading_pair relationship
                # For now, we'll use a placeholder price
                current_price = Decimal('50000')  # Placeholder price
                
                should_trigger = False
                
                # Check trigger conditions
                if alert.alert_type == 'price_above' and alert.target_price and current_price > alert.target_price:
                    should_trigger = True
                elif alert.alert_type == 'price_below' and alert.target_price and current_price < alert.target_price:
                    should_trigger = True
                
                if should_trigger:
                    # Create trigger
                    from .models import AlertTrigger
                    trigger = AlertTrigger.objects.create(
                        alert=alert,
                        triggered_price=current_price,
                        trigger_conditions={'current_price': float(current_price)},
                    )
                    
                    # Send notification
                    send_notification.delay(alert.user.id, alert.id)
                    
                    # Update alert status
                    alert.status = 'triggered'
                    alert.triggered_at = timezone.now()
                    alert.save()
                    
            except Exception as e:
                logger.error(f"Error processing price alert {alert.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in process_price_alerts: {str(e)}")
        raise

@shared_task
def process_trading_signals():
    """Process trading signals"""
    try:
        from .models import TradingSignal
        
        # Get active trading signals
        signals = TradingSignal.objects.filter(
            is_active=True,
            created_at__gte=timezone.now() - timezone.timedelta(hours=24)  # Recent signals only
        )
        
        for signal in signals:
            try:
                # Check if signal has expired
                if signal.expires_at and timezone.now() > signal.expires_at:
                    signal.is_active = False
                    signal.save()
                    
            except Exception as e:
                logger.error(f"Error processing trading signal {signal.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in process_trading_signals: {str(e)}")
        raise

@shared_task
def process_alert_triggers():
    """Process various alert triggers"""
    try:
        from .models import Alert
        from portfolio_management.models import Portfolio
        
        # Get portfolio value alerts
        portfolio_alerts = Alert.objects.filter(
            alert_type='portfolio_alert',
            status='active'
        ).select_related('user')
        
        for alert in portfolio_alerts:
            try:
                portfolio = Portfolio.objects.filter(user=alert.user).first()
                if not portfolio:
                    continue
                
                current_value = portfolio.total_value
                should_trigger = False
                
                # Check trigger conditions
                if alert.target_price:
                    if alert.alert_type == 'portfolio_alert' and current_value > alert.target_price:
                        should_trigger = True
                
                if should_trigger:
                    # Create trigger
                    from .models import AlertTrigger
                    trigger = AlertTrigger.objects.create(
                        alert=alert,
                        triggered_price=current_value,
                        trigger_conditions={'portfolio_value': float(current_value)},
                    )
                    
                    # Send notification
                    send_notification.delay(alert.user.id, alert.id)
                    
                    # Update alert status
                    alert.status = 'triggered'
                    alert.triggered_at = timezone.now()
                    alert.save()
                    
            except Exception as e:
                logger.error(f"Error processing portfolio alert {alert.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in process_alert_triggers: {str(e)}")
        raise

@shared_task
def process_market_alerts():
    """Process market-wide alerts"""
    try:
        from .models import MarketAlert
        
        # Check for market-wide events
        # For now, just log that we're processing market alerts
        logger.info("Processing market alerts")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in process_market_alerts: {str(e)}")
        raise

@shared_task
def notify_subscribed_users(alert_id):
    """Notify users subscribed to market alerts"""
    try:
        from .models import MarketAlert, AlertSubscription
        
        alert = MarketAlert.objects.get(id=alert_id)
        
        # Get subscribed users
        subscriptions = AlertSubscription.objects.filter(
            is_active=True
        ).select_related('user')
        
        for subscription in subscriptions:
            try:
                # Send notification to user
                send_market_alert_notification.delay(subscription.user.id, alert.id)
                
            except Exception as e:
                logger.error(f"Error notifying user {subscription.user.id}: {str(e)}")
                continue
        
        return True
        
    except MarketAlert.DoesNotExist:
        logger.error(f"Market alert {alert_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error notifying subscribed users: {str(e)}")
        raise

@shared_task
def send_notification(user_id, alert_id):
    """Send notification to user"""
    try:
        from accounts.models import User
        from .models import Alert
        
        user = User.objects.get(id=user_id)
        alert = Alert.objects.get(id=alert_id)
        
        # Send email notification
        send_email_notification.delay(user.email, alert.name, alert.message)
        
        # Send push notification (if implemented)
        send_push_notification.delay(user.id, alert.name, alert.message)
        
        # Send WebSocket notification
        send_websocket_notification.delay(user.id, alert.id)
        
        logger.info(f"Sent notification to user {user_id} for alert {alert_id}")
        return True
        
    except (User.DoesNotExist, Alert.DoesNotExist) as e:
        logger.error(f"User or alert not found: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        raise

@shared_task
def send_trading_signal_notification(signal_id):
    """Send trading signal notification"""
    try:
        from .models import TradingSignal
        
        signal = TradingSignal.objects.get(id=signal_id)
        
        # For now, just log the signal
        logger.info(f"Trading signal {signal_id}: {signal.signal_type} for {signal.trading_pair}")
        
        return True
        
    except TradingSignal.DoesNotExist:
        logger.error(f"Trading signal {signal_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending trading signal notification: {str(e)}")
        raise

@shared_task
def send_market_alert_notification(user_id, alert_id):
    """Send market alert notification"""
    try:
        from .models import MarketAlert
        
        alert = MarketAlert.objects.get(id=alert_id)
        
        # Create user-specific alert
        from .models import Alert
        user_alert = Alert.objects.create(
            user_id=user_id,
            name=alert.title,
            alert_type='custom',
            message=alert.message,
            status='active',
        )
        
        # Send notification
        send_notification.delay(user_id, user_alert.id)
        
        return True
        
    except MarketAlert.DoesNotExist:
        logger.error(f"Market alert {alert_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending market alert notification: {str(e)}")
        raise

@shared_task
def send_email_notification(email, subject, message):
    """Send email notification"""
    try:
        from django.core.mail import send_mail
        from django.conf import settings
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        
        logger.info(f"Email notification sent to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email notification: {str(e)}")
        raise

@shared_task
def send_push_notification(user_id, title, message):
    """Send push notification"""
    try:
        # This would integrate with a push notification service
        # For now, just log the notification
        logger.info(f"Push notification for user {user_id}: {title} - {message}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending push notification: {str(e)}")
        raise

@shared_task
def send_websocket_notification(user_id, alert_id):
    """Send WebSocket notification"""
    try:
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "alert.notification",
                "alert_id": alert_id,
            }
        )
        
        logger.info(f"WebSocket notification sent to user {user_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending WebSocket notification: {str(e)}")
        raise 