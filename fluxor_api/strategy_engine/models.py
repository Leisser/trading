"""
Strategy Engine Models for Automated Trading Strategies
"""
from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


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
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('stopped', 'Stopped'),
        ('completed', 'Completed')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_strategies')
    name = models.CharField(max_length=100)
    description = models.TextField()
    strategy_type = models.CharField(max_length=20, choices=STRATEGY_TYPE_CHOICES)
    
    # Strategy parameters
    symbol = models.CharField(max_length=20)  # e.g., BTC/USDT
    is_active = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='paused')
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
    started_at = models.DateTimeField(null=True, blank=True)
    stopped_at = models.DateTimeField(null=True, blank=True)
    
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
        if self.total_trades > 0:
            return (self.winning_trades / self.total_trades) * 100
        return 0
    
    @property
    def win_rate(self):
        return self.calculate_win_rate()


class StrategyExecution(models.Model):
    """Track individual strategy executions"""
    
    ACTION_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('hold', 'Hold'),
        ('stop', 'Stop'),
        ('adjust', 'Adjust Position')
    ]
    
    strategy = models.ForeignKey(TradingStrategy, on_delete=models.CASCADE, related_name='executions')
    execution_time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    symbol = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    reason = models.TextField()
    pnl = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    
    # Execution metadata
    market_conditions = models.JSONField(default=dict)  # Store market data at execution time
    strategy_parameters = models.JSONField(default=dict)  # Store strategy parameters at execution time
    
    class Meta:
        ordering = ['-execution_time']
    
    def __str__(self):
        return f"{self.strategy.name} - {self.action} {self.symbol} at {self.execution_time}"


class StrategyPerformance(models.Model):
    """Track strategy performance over time"""
    
    strategy = models.ForeignKey(TradingStrategy, on_delete=models.CASCADE, related_name='performance_records')
    date = models.DateField()
    
    # Daily performance metrics
    daily_pnl = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    daily_trades = models.IntegerField(default=0)
    daily_win_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0'))
    
    # Cumulative metrics
    cumulative_pnl = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    cumulative_trades = models.IntegerField(default=0)
    cumulative_win_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0'))
    
    # Risk metrics
    max_drawdown = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0'))
    sharpe_ratio = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0'))
    volatility = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['strategy', 'date']
    
    def __str__(self):
        return f"{self.strategy.name} - {self.date} (PnL: {self.daily_pnl})"


class StrategyAlert(models.Model):
    """Alerts for strategy events"""
    
    ALERT_TYPES = [
        ('profit_target', 'Profit Target Reached'),
        ('stop_loss', 'Stop Loss Triggered'),
        ('position_limit', 'Position Limit Reached'),
        ('strategy_error', 'Strategy Error'),
        ('market_condition', 'Market Condition Change'),
        ('custom', 'Custom Alert')
    ]
    
    strategy = models.ForeignKey(TradingStrategy, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    
    # Alert data
    alert_data = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.strategy.name} - {self.title}"
