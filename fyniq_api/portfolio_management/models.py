from django.db import models
from django.conf import settings
from decimal import Decimal
from django.utils import timezone

class Portfolio(models.Model):
    """Model for user portfolios"""
    
    PORTFOLIO_TYPES = [
        ('spot', 'Spot Trading'),
        ('margin', 'Margin Trading'),
        ('futures', 'Futures Trading'),
        ('options', 'Options Trading'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100)
    portfolio_type = models.CharField(max_length=20, choices=PORTFOLIO_TYPES, default='spot')
    description = models.TextField(blank=True)
    
    # Portfolio settings
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    # Risk management
    max_position_size = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    max_leverage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stop_loss_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'name']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.user.email} - {self.name} ({self.portfolio_type})"

class Position(models.Model):
    """Model for trading positions"""
    
    POSITION_SIDES = [
        ('long', 'Long'),
        ('short', 'Short'),
    ]
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='positions')
    trading_pair = models.CharField(max_length=20)
    base_currency = models.CharField(max_length=10)
    quote_currency = models.CharField(max_length=10)
    
    # Position details
    side = models.CharField(max_length=5, choices=POSITION_SIDES)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    average_entry_price = models.DecimalField(max_digits=20, decimal_places=8)
    current_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    
    # P&L calculations
    unrealized_pnl = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    realized_pnl = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    total_pnl = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    
    # Position value
    position_value = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    margin_used = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    
    # Risk management
    stop_loss_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    take_profit_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    leverage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1'))
    
    # Status
    is_open = models.BooleanField(default=True)
    is_hedged = models.BooleanField(default=False)
    
    # Timestamps
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['portfolio', 'trading_pair', 'side']
        ordering = ['-opened_at']
        indexes = [
            models.Index(fields=['portfolio', 'is_open']),
            models.Index(fields=['trading_pair', 'is_open']),
        ]
    
    def __str__(self):
        return f"{self.trading_pair} {self.side} {self.quantity} @ {self.average_entry_price}"
    
    @property
    def market_value(self):
        """Calculate current market value of position"""
        if self.current_price:
            return self.quantity * self.current_price
        return self.position_value
    
    @property
    def pnl_percentage(self):
        """Calculate P&L as percentage"""
        if self.average_entry_price and self.average_entry_price > 0:
            if self.side == 'long' and self.current_price:
                return ((self.current_price - self.average_entry_price) / self.average_entry_price) * 100
            elif self.side == 'short' and self.current_price:
                return ((self.average_entry_price - self.current_price) / self.average_entry_price) * 100
        return Decimal('0')

class PortfolioBalance(models.Model):
    """Model for portfolio balances"""
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='balances')
    currency = models.CharField(max_length=10)
    
    # Balance amounts
    available_balance = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    locked_balance = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    total_balance = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    
    # USD equivalent
    usd_value = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0'))
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['portfolio', 'currency']
        ordering = ['currency']
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.currency}: {self.total_balance}"

class PortfolioSnapshot(models.Model):
    """Model for portfolio snapshots for historical tracking"""
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='snapshots')
    timestamp = models.DateTimeField()
    
    # Portfolio metrics
    total_value = models.DecimalField(max_digits=20, decimal_places=2)
    total_pnl = models.DecimalField(max_digits=20, decimal_places=2)
    daily_pnl = models.DecimalField(max_digits=20, decimal_places=2)
    weekly_pnl = models.DecimalField(max_digits=20, decimal_places=2)
    monthly_pnl = models.DecimalField(max_digits=20, decimal_places=2)
    
    # Risk metrics
    sharpe_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    max_drawdown = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    volatility = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    # Position data
    open_positions = models.IntegerField(default=0)
    total_positions = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['portfolio', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.timestamp}: ${self.total_value}"

class PortfolioPerformance(models.Model):
    """Model for portfolio performance metrics"""
    
    PERFORMANCE_PERIODS = [
        ('1d', '1 Day'),
        ('1w', '1 Week'),
        ('1m', '1 Month'),
        ('3m', '3 Months'),
        ('6m', '6 Months'),
        ('1y', '1 Year'),
        ('all', 'All Time'),
    ]
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='performance')
    period = models.CharField(max_length=3, choices=PERFORMANCE_PERIODS)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Performance metrics
    total_return = models.DecimalField(max_digits=10, decimal_places=4)  # Percentage
    absolute_return = models.DecimalField(max_digits=20, decimal_places=2)  # USD
    sharpe_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    sortino_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    max_drawdown = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    volatility = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    beta = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    alpha = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    # Trading metrics
    total_trades = models.IntegerField(default=0)
    winning_trades = models.IntegerField(default=0)
    losing_trades = models.IntegerField(default=0)
    win_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0'))
    average_trade = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0'))
    
    # Timestamps
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['portfolio', 'period', 'start_date']
        ordering = ['-end_date']
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.period}: {self.total_return}%"

class AssetAllocation(models.Model):
    """Model for asset allocation tracking"""
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='allocations')
    currency = models.CharField(max_length=10)
    
    # Allocation data
    allocation_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    allocation_value = models.DecimalField(max_digits=20, decimal_places=2)
    
    # Performance
    currency_return = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0'))
    contribution_to_return = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0'))
    
    # Timestamps
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['portfolio', 'currency', 'date']
        ordering = ['-date', 'allocation_percentage']
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.currency}: {self.allocation_percentage}%"
