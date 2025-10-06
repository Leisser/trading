"""
Portfolio Management Models
"""
from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class Portfolio(models.Model):
    """Model for user portfolios"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.name}"


class PortfolioBalance(models.Model):
    """Model for portfolio balances"""
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='balances')
    symbol = models.CharField(max_length=20)  # e.g., BTC, ETH, USD
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    current_value = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0'))
    average_cost = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['portfolio', 'symbol']
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.symbol}: {self.balance}"


class Transaction(models.Model):
    """Model for portfolio transactions"""
    
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('trade', 'Trade'),
        ('dividend', 'Dividend'),
        ('fee', 'Fee'),
        ('transfer', 'Transfer'),
    ]
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    symbol = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    fees = models.DecimalField(max_digits=10, decimal_places=8, default=Decimal('0'))
    notes = models.TextField(blank=True)
    
    transaction_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-transaction_date']
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.transaction_type} {self.amount} {self.symbol}"


class PnLRecord(models.Model):
    """Model for profit and loss records"""
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='pnl_records')
    date = models.DateField()
    
    # P&L metrics
    total_pnl = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0'))
    realized_pnl = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0'))
    unrealized_pnl = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0'))
    
    # Performance metrics
    total_return = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0'))
    daily_return = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0'))
    
    # Risk metrics
    max_drawdown = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0'))
    volatility = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0'))
    sharpe_ratio = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['portfolio', 'date']
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.date} (PnL: {self.total_pnl})"


class AssetAllocation(models.Model):
    """Model for asset allocation tracking"""
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='allocations')
    symbol = models.CharField(max_length=20)
    allocation_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0'))
    target_allocation = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0'))
    current_value = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0'))
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['portfolio', 'symbol']
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.symbol}: {self.allocation_percentage}%"
