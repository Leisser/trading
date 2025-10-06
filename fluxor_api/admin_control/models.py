"""
Admin Control Models for Profit/Loss Scenarios and Trading Settings
"""
from django.db import models
from django.contrib.auth import get_user_model
from trades.models import CryptoIndex, Cryptocurrency

User = get_user_model()


class TradingSettings(models.Model):
    """Global trading settings controlled by admin"""
    
    PROFIT_LOSS_MODES = [
        ('manual', 'Manual Control'),
        ('automatic', 'Automatic Based on Market'),
        ('simulated', 'Simulated Trading'),
        ('custom', 'Custom Scenarios'),
    ]
    
    # Global Settings
    trading_enabled = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    profit_loss_mode = models.CharField(max_length=10, choices=PROFIT_LOSS_MODES, default='automatic')
    
    # Default Rates
    default_profit_rate = models.DecimalField(max_digits=10, decimal_places=4, default=5.0)  # % per hour
    default_loss_rate = models.DecimalField(max_digits=10, decimal_places=4, default=2.0)  # % per hour
    max_profit_rate = models.DecimalField(max_digits=10, decimal_places=4, default=100.0)
    max_loss_rate = models.DecimalField(max_digits=10, decimal_places=4, default=50.0)
    
    # Index Settings
    index_appreciation_rate = models.DecimalField(max_digits=10, decimal_places=4, default=10.0)  # % per day
    index_depreciation_rate = models.DecimalField(max_digits=10, decimal_places=4, default=5.0)  # % per day
    index_volatility_factor = models.DecimalField(max_digits=5, decimal_places=2, default=1.5)
    
    # Update Frequencies (in seconds)
    price_update_frequency = models.IntegerField(default=1)  # Every 1 second
    investment_update_frequency = models.IntegerField(default=5)  # Every 5 seconds
    portfolio_calculation_frequency = models.IntegerField(default=10)  # Every 10 seconds
    
    # Trading Limits
    min_trade_amount = models.DecimalField(max_digits=20, decimal_places=8, default=0.001)
    max_trade_amount = models.DecimalField(max_digits=20, decimal_places=8, default=100.0)
    min_investment_amount = models.DecimalField(max_digits=20, decimal_places=8, default=0.01)
    
    # Fees
    trading_fee_percentage = models.DecimalField(max_digits=5, decimal_places=4, default=0.001)  # 0.1%
    withdrawal_fee_percentage = models.DecimalField(max_digits=5, decimal_places=4, default=0.005)  # 0.5%
    management_fee_percentage = models.DecimalField(max_digits=5, decimal_places=4, default=0.02)  # 2% annually
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Trading Settings"
        verbose_name_plural = "Trading Settings"
    
    def __str__(self):
        return f"Trading Settings - {self.updated_at}"


class ProfitLossScenario(models.Model):
    """Custom profit/loss scenarios for admin control"""
    
    SCENARIO_TYPES = [
        ('profit', 'Profit Scenario'),
        ('loss', 'Loss Scenario'),
        ('mixed', 'Mixed Scenario'),
    ]
    
    TIME_UNITS = [
        ('seconds', 'Seconds'),
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    scenario_type = models.CharField(max_length=10, choices=SCENARIO_TYPES)
    
    # Profit/Loss Parameters
    percentage_change = models.DecimalField(max_digits=10, decimal_places=4)  # +100 for 100% profit, -50 for 50% loss
    time_duration = models.IntegerField()  # Duration value
    time_unit = models.CharField(max_length=10, choices=TIME_UNITS)
    
    # Target Settings
    target_crypto_index = models.ForeignKey(CryptoIndex, on_delete=models.CASCADE, null=True, blank=True, related_name='admin_scenarios')
    target_cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, null=True, blank=True, related_name='admin_scenarios')
    apply_to_all_investments = models.BooleanField(default=False)
    apply_to_all_users = models.BooleanField(default=False)
    
    # Execution Settings
    is_active = models.BooleanField(default=False)
    execute_immediately = models.BooleanField(default=False)
    scheduled_execution = models.DateTimeField(null=True, blank=True)
    repeat_execution = models.BooleanField(default=False)
    repeat_interval_hours = models.IntegerField(default=24)
    
    # Tracking
    times_executed = models.IntegerField(default=0)
    last_executed = models.DateTimeField(null=True, blank=True)
    next_execution = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_admin_scenarios')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Profit/Loss Scenario"
        verbose_name_plural = "Profit/Loss Scenarios"
    
    def __str__(self):
        return f"{self.name} - {self.percentage_change}% in {self.time_duration} {self.time_unit}"
    
    @property
    def duration_in_seconds(self):
        """Convert time duration to seconds"""
        multipliers = {
            'seconds': 1,
            'minutes': 60,
            'hours': 3600,
            'days': 86400,
            'weeks': 604800,
            'months': 2592000,  # Approximate
        }
        return self.time_duration * multipliers.get(self.time_unit, 1)


class ScenarioExecution(models.Model):
    """Track scenario executions"""
    
    scenario = models.ForeignKey(ProfitLossScenario, on_delete=models.CASCADE, related_name='executions')
    executed_at = models.DateTimeField(auto_now_add=True)
    executed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Execution details
    affected_investments = models.IntegerField(default=0)
    affected_users = models.IntegerField(default=0)
    total_value_change = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('success', 'Success'),
        ('partial', 'Partial Success'),
        ('failed', 'Failed'),
    ], default='success')
    
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-executed_at']
    
    def __str__(self):
        return f"{self.scenario.name} - {self.executed_at} ({self.status})"
