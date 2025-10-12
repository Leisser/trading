from django.db import models
from django.utils import timezone
from decimal import Decimal

class Exchange(models.Model):
    """Model for cryptocurrency exchanges"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    api_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class TradingPair(models.Model):
    """Model for trading pairs"""
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='trading_pairs')
    base_currency = models.CharField(max_length=10)  # e.g., BTC
    quote_currency = models.CharField(max_length=10)  # e.g., USD
    symbol = models.CharField(max_length=20)  # e.g., BTC/USD
    is_active = models.BooleanField(default=True)
    min_order_size = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    max_order_size = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    price_precision = models.IntegerField(default=2)
    quantity_precision = models.IntegerField(default=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['exchange', 'symbol']
        ordering = ['symbol']
    
    def __str__(self):
        return f"{self.symbol} on {self.exchange.name}"

class MarketData(models.Model):
    """Model for storing market data"""
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, related_name='market_data')
    timestamp = models.DateTimeField()
    open_price = models.DecimalField(max_digits=20, decimal_places=8)
    high_price = models.DecimalField(max_digits=20, decimal_places=8)
    low_price = models.DecimalField(max_digits=20, decimal_places=8)
    close_price = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=20, decimal_places=8)
    quote_volume = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    number_of_trades = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['trading_pair', 'timestamp']
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['trading_pair', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.trading_pair.symbol} - {self.timestamp}"

class Ticker(models.Model):
    """Model for storing ticker data"""
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, related_name='tickers')
    timestamp = models.DateTimeField()
    last_price = models.DecimalField(max_digits=20, decimal_places=8)
    bid_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    ask_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    bid_volume = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    ask_volume = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    high_24h = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    low_24h = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    price_change_24h = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    price_change_percent_24h = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['trading_pair', 'timestamp']
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['trading_pair', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.trading_pair.symbol} - {self.last_price} at {self.timestamp}"

class OrderBook(models.Model):
    """Model for storing order book data"""
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, related_name='order_books')
    timestamp = models.DateTimeField()
    side = models.CharField(max_length=4, choices=[('bid', 'Bid'), ('ask', 'Ask')])
    price = models.DecimalField(max_digits=20, decimal_places=8)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp', 'side', 'price']
        indexes = [
            models.Index(fields=['trading_pair', 'timestamp']),
            models.Index(fields=['trading_pair', 'side', 'price']),
        ]
    
    def __str__(self):
        return f"{self.trading_pair.symbol} {self.side} {self.quantity} @ {self.price}"

class Trade(models.Model):
    """Model for storing trade data"""
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, related_name='trades')
    exchange_trade_id = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField()
    side = models.CharField(max_length=4, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    price = models.DecimalField(max_digits=20, decimal_places=8)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    quote_quantity = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    fee = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    fee_currency = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['trading_pair', 'timestamp']),
            models.Index(fields=['exchange_trade_id']),
        ]
    
    def __str__(self):
        return f"{self.trading_pair.symbol} {self.side} {self.quantity} @ {self.price}"

class MarketDataAggregation(models.Model):
    """Model for aggregated market data across exchanges"""
    base_currency = models.CharField(max_length=10)
    quote_currency = models.CharField(max_length=10)
    symbol = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    weighted_average_price = models.DecimalField(max_digits=20, decimal_places=8)
    total_volume = models.DecimalField(max_digits=20, decimal_places=8)
    number_of_exchanges = models.IntegerField()
    price_volatility = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['symbol', 'timestamp']
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['symbol', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.symbol} - {self.weighted_average_price} at {self.timestamp}"

class ChartDataPoint(models.Model):
    """
    Model for storing chart data points with automatic 24-hour cleanup.
    This is a simplified model specifically for frontend chart display.
    """
    symbol = models.CharField(max_length=10, help_text="Cryptocurrency symbol (e.g., BTC, ETH)")
    timestamp = models.DateTimeField(help_text="Data point timestamp")
    open_price = models.DecimalField(max_digits=20, decimal_places=8)
    high_price = models.DecimalField(max_digits=20, decimal_places=8)
    low_price = models.DecimalField(max_digits=20, decimal_places=8)
    close_price = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    source = models.CharField(
        max_length=20, 
        choices=[
            ('real', 'Real Exchange Data'),
            ('simulated', 'Simulated Data'),
            ('hybrid', 'Mixed Real/Simulated')
        ],
        default='simulated',
        help_text="Data source type"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['symbol', 'timestamp']),
            models.Index(fields=['timestamp']),  # For cleanup queries
            models.Index(fields=['created_at']),  # For cleanup queries
        ]
        unique_together = ['symbol', 'timestamp']
    
    def __str__(self):
        return f"{self.symbol} - {self.close_price} at {self.timestamp}"
    
    @classmethod
    def cleanup_old_data(cls, hours=24):
        """
        Delete chart data points older than specified hours.
        This method is called by Celery task for automatic cleanup.
        """
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_time = timezone.now() - timedelta(hours=hours)
        deleted_count, _ = cls.objects.filter(timestamp__lt=cutoff_time).delete()
        return deleted_count
    
    @classmethod
    def get_latest_data(cls, symbol, limit=30):
        """Get latest chart data for a symbol"""
        return cls.objects.filter(symbol=symbol).order_by('-timestamp')[:limit]

class PriceAlert(models.Model):
    """Model for price alerts"""
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='price_alerts')
    symbol = models.CharField(max_length=20)
    target_price = models.DecimalField(max_digits=20, decimal_places=8)
    condition = models.CharField(max_length=5, choices=[('above', 'Above'), ('below', 'Below')])
    message = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_triggered = models.BooleanField(default=False)
    triggered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['symbol', 'is_active', 'is_triggered']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.symbol} {self.condition} {self.target_price}"
    
    def trigger_alert(self):
        """Mark alert as triggered"""
        self.is_triggered = True
        self.triggered_at = timezone.now()
        self.is_active = False
        self.save()
