"""
Advanced Trading Models for sophisticated order types and strategies.
"""
from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderType(models.Model):
    """Model for different order types"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class AdvancedOrder(models.Model):
    """Model for advanced trading orders"""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('filled', 'Filled'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('rejected', 'Rejected')
    ]
    
    ORDER_TYPE_CHOICES = [
        ('market', 'Market Order'),
        ('limit', 'Limit Order'),
        ('stop_loss', 'Stop Loss'),
        ('take_profit', 'Take Profit'),
        ('stop_limit', 'Stop Limit'),
        ('trailing_stop', 'Trailing Stop')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advanced_orders')
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)
    symbol = models.CharField(max_length=20)  # e.g., BTC/USDT
    side = models.CharField(max_length=4, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    
    # Order parameters
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)  # For limit orders
    stop_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)  # For stop orders
    limit_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)  # For stop-limit orders
    
    # Advanced parameters
    time_in_force = models.CharField(max_length=10, choices=[
        ('GTC', 'Good Till Cancelled'),
        ('IOC', 'Immediate or Cancel'),
        ('FOK', 'Fill or Kill'),
        ('GTD', 'Good Till Date')
    ], default='GTC')
    expire_time = models.DateTimeField(null=True, blank=True)
    
    # Trailing stop parameters
    trailing_distance = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    trailing_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Order status and execution
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    filled_quantity = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    average_fill_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    total_fees = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    filled_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    # Additional metadata
    notes = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['symbol', 'status']),
            models.Index(fields=['order_type', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.symbol} {self.side} {self.quantity} ({self.order_type})"
    
    def is_filled(self):
        """Check if order is completely filled"""
        return self.status == 'filled'
    
    def is_pending(self):
        """Check if order is pending"""
        return self.status == 'pending'
    
    def can_cancel(self):
        """Check if order can be cancelled"""
        return self.status == 'pending'
    
    def calculate_remaining_quantity(self):
        """Calculate remaining quantity to be filled"""
        return self.quantity - self.filled_quantity
    
    def calculate_fill_percentage(self):
        """Calculate percentage of order filled"""
        if self.quantity == 0:
            return 0
        return (self.filled_quantity / self.quantity) * 100

class TradingStrategy(models.Model):
    """Model for automated trading strategies"""
    STRATEGY_TYPE_CHOICES = [
        ('dca', 'Dollar Cost Averaging'),
        ('grid', 'Grid Trading'),
        ('momentum', 'Momentum Trading'),
        ('mean_reversion', 'Mean Reversion'),
        ('arbitrage', 'Arbitrage'),
        ('custom', 'Custom Strategy')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_strategies')
    name = models.CharField(max_length=100)
    description = models.TextField()
    strategy_type = models.CharField(max_length=20, choices=STRATEGY_TYPE_CHOICES)
    
    # Strategy parameters
    symbol = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    parameters = models.JSONField(default=dict)  # Strategy-specific parameters
    
    # Risk management
    max_position_size = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    stop_loss_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    take_profit_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Performance tracking
    total_trades = models.IntegerField(default=0)
    winning_trades = models.IntegerField(default=0)
    losing_trades = models.IntegerField(default=0)
    total_pnl = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_executed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['strategy_type', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.name} ({self.strategy_type})"
    
    def calculate_win_rate(self):
        """Calculate win rate percentage"""
        if self.total_trades == 0:
            return 0
        return (self.winning_trades / self.total_trades) * 100
    
    def calculate_avg_pnl(self):
        """Calculate average P&L per trade"""
        if self.total_trades == 0:
            return 0
        return self.total_pnl / self.total_trades

class OrderExecution(models.Model):
    """Model for tracking order executions"""
    order = models.ForeignKey(AdvancedOrder, on_delete=models.CASCADE, related_name='executions')
    execution_time = models.DateTimeField()
    executed_quantity = models.DecimalField(max_digits=20, decimal_places=8)
    execution_price = models.DecimalField(max_digits=20, decimal_places=8)
    fees = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    exchange_order_id = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-execution_time']
        indexes = [
            models.Index(fields=['order', 'execution_time']),
        ]
    
    def __str__(self):
        return f"{self.order.symbol} - {self.executed_quantity} @ {self.execution_price}"

class StrategyExecution(models.Model):
    """Model for tracking strategy executions"""
    strategy = models.ForeignKey(TradingStrategy, on_delete=models.CASCADE, related_name='executions')
    execution_time = models.DateTimeField()
    action = models.CharField(max_length=20, choices=[
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('hold', 'Hold')
    ])
    symbol = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    reason = models.TextField(blank=True)
    pnl = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    
    class Meta:
        ordering = ['-execution_time']
        indexes = [
            models.Index(fields=['strategy', 'execution_time']),
        ]
    
    def __str__(self):
        return f"{self.strategy.name} - {self.action} {self.symbol} at {self.execution_time}"
