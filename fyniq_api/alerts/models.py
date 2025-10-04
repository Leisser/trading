from django.db import models
from django.conf import settings
from decimal import Decimal
from django.utils import timezone

class Alert(models.Model):
    """Model for user alerts"""
    
    ALERT_TYPES = [
        ('price_above', 'Price Above'),
        ('price_below', 'Price Below'),
        ('price_change', 'Price Change'),
        ('volume_spike', 'Volume Spike'),
        ('technical_signal', 'Technical Signal'),
        ('news_alert', 'News Alert'),
        ('portfolio_alert', 'Portfolio Alert'),
        ('custom', 'Custom Alert'),
    ]
    
    ALERT_STATUS = [
        ('active', 'Active'),
        ('triggered', 'Triggered'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic alert information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alerts')
    name = models.CharField(max_length=100)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    
    # Alert target
    trading_pair = models.CharField(max_length=20, null=True, blank=True)
    target_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    price_change_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Alert conditions
    conditions = models.JSONField(default=dict, blank=True)  # Flexible conditions storage
    message = models.TextField(blank=True)
    
    # Alert settings
    status = models.CharField(max_length=20, choices=ALERT_STATUS, default='active')
    is_recurring = models.BooleanField(default=False)
    repeat_interval = models.IntegerField(null=True, blank=True)  # minutes
    
    # Notification settings
    notify_email = models.BooleanField(default=True)
    notify_sms = models.BooleanField(default=False)
    notify_push = models.BooleanField(default=True)
    notify_in_app = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    triggered_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['trading_pair', 'status']),
            models.Index(fields=['alert_type', 'status']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.alert_type} ({self.status})"
    
    @property
    def is_expired(self):
        """Check if alert has expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    @property
    def is_active(self):
        """Check if alert is currently active"""
        return self.status == 'active' and not self.is_expired

class TradingSignal(models.Model):
    """Model for trading signals"""
    
    SIGNAL_TYPES = [
        ('buy', 'Buy Signal'),
        ('sell', 'Sell Signal'),
        ('hold', 'Hold Signal'),
        ('strong_buy', 'Strong Buy'),
        ('strong_sell', 'Strong Sell'),
    ]
    
    SIGNAL_SOURCES = [
        ('technical_analysis', 'Technical Analysis'),
        ('fundamental_analysis', 'Fundamental Analysis'),
        ('sentiment_analysis', 'Sentiment Analysis'),
        ('ai_model', 'AI Model'),
        ('expert_opinion', 'Expert Opinion'),
        ('news_event', 'News Event'),
    ]
    
    SIGNAL_STRENGTH = [
        ('weak', 'Weak'),
        ('moderate', 'Moderate'),
        ('strong', 'Strong'),
        ('very_strong', 'Very Strong'),
    ]
    
    # Signal information
    trading_pair = models.CharField(max_length=20)
    signal_type = models.CharField(max_length=20, choices=SIGNAL_TYPES)
    signal_source = models.CharField(max_length=20, choices=SIGNAL_SOURCES)
    signal_strength = models.CharField(max_length=20, choices=SIGNAL_STRENGTH)
    
    # Signal details
    current_price = models.DecimalField(max_digits=20, decimal_places=8)
    target_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    stop_loss_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    take_profit_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    
    # Analysis data
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100
    analysis_data = models.JSONField(default=dict, blank=True)
    reasoning = models.TextField(blank=True)
    
    # Signal metadata
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['trading_pair', 'signal_type']),
            models.Index(fields=['signal_source', 'is_active']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.trading_pair} {self.signal_type} ({self.signal_strength})"

class AlertTrigger(models.Model):
    """Model for alert trigger history"""
    
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='triggers')
    signal = models.ForeignKey(TradingSignal, on_delete=models.SET_NULL, null=True, blank=True, related_name='alert_triggers')
    
    # Trigger details
    triggered_price = models.DecimalField(max_digits=20, decimal_places=8)
    trigger_conditions = models.JSONField(default=dict)
    
    # Notification status
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    push_sent = models.BooleanField(default=False)
    in_app_sent = models.BooleanField(default=False)
    
    # Timestamps
    triggered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-triggered_at']
        indexes = [
            models.Index(fields=['alert', 'triggered_at']),
            models.Index(fields=['triggered_at']),
        ]
    
    def __str__(self):
        return f"{self.alert.name} triggered at {self.triggered_at}"

class AlertSubscription(models.Model):
    """Model for alert subscriptions"""
    
    SUBSCRIPTION_TYPES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alert_subscriptions')
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, default='free')
    
    # Subscription limits
    max_alerts = models.IntegerField(default=5)
    max_signals = models.IntegerField(default=10)
    advanced_features = models.BooleanField(default=False)
    
    # Subscription status
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    # Usage tracking
    alerts_used = models.IntegerField(default=0)
    signals_accessed = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.user.email} - {self.subscription_type}"

class MarketAlert(models.Model):
    """Model for market-wide alerts"""
    
    ALERT_CATEGORIES = [
        ('market_crash', 'Market Crash'),
        ('bull_run', 'Bull Run'),
        ('high_volatility', 'High Volatility'),
        ('low_liquidity', 'Low Liquidity'),
        ('exchange_issue', 'Exchange Issue'),
        ('regulatory_news', 'Regulatory News'),
        ('security_alert', 'Security Alert'),
    ]
    
    SEVERITY_LEVELS = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('emergency', 'Emergency'),
    ]
    
    # Alert information
    category = models.CharField(max_length=20, choices=ALERT_CATEGORIES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Affected markets
    affected_pairs = models.JSONField(default=list, blank=True)
    affected_exchanges = models.JSONField(default=list, blank=True)
    
    # Alert settings
    is_active = models.BooleanField(default=True)
    is_global = models.BooleanField(default=False)
    requires_acknowledgment = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['severity', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.category} - {self.title} ({self.severity})"

class UserAlertPreference(models.Model):
    """Model for user alert preferences"""
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alert_preferences')
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
    in_app_notifications = models.BooleanField(default=True)
    
    # Alert frequency
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Alert filters
    min_priority = models.CharField(max_length=10, choices=Alert.PRIORITY_LEVELS, default='low')
    excluded_pairs = models.JSONField(default=list, blank=True)
    excluded_types = models.JSONField(default=list, blank=True)
    
    # Advanced settings
    batch_notifications = models.BooleanField(default=True)
    notification_delay = models.IntegerField(default=0)  # minutes
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Alert Preference'
        verbose_name_plural = 'User Alert Preferences'
    
    def __str__(self):
        return f"Alert preferences for {self.user.email}"
