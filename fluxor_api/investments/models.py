"""
Investment Management Models
"""
from django.db import models
from django.contrib.auth import get_user_model
from trades.models import Cryptocurrency, CryptoIndex

User = get_user_model()


class Investment(models.Model):
    """Model for user investments in crypto indices or individual cryptocurrencies"""
    
    INVESTMENT_TYPES = [
        ('index', 'Index Investment'),
        ('single_crypto', 'Single Cryptocurrency'),
        ('dca', 'Dollar Cost Averaging'),
        ('hodl', 'Long-term Hold'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('closed', 'Closed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    investment_type = models.CharField(max_length=15, choices=INVESTMENT_TYPES, default='index')
    
    # Investment target (either index or single crypto)
    crypto_index = models.ForeignKey(CryptoIndex, on_delete=models.CASCADE, null=True, blank=True, related_name='investment_portfolio')
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, null=True, blank=True, related_name='investment_portfolio')
    
    # Investment details
    name = models.CharField(max_length=100)  # User-defined name for this investment
    total_invested_btc = models.DecimalField(max_digits=20, decimal_places=8, default=0)  # Total BTC invested
    total_invested_usd = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # USD value at investment time
    current_value_btc = models.DecimalField(max_digits=20, decimal_places=8, default=0)  # Current BTC value
    current_value_usd = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # Current USD value
    
    # Performance tracking
    unrealized_pnl_btc = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    unrealized_pnl_usd = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    unrealized_pnl_percent = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    all_time_high_value = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    max_drawdown_percent = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    # Investment strategy settings
    auto_compound = models.BooleanField(default=False)  # Reinvest gains
    dca_amount_btc = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    dca_frequency = models.CharField(max_length=10, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], blank=True)
    next_dca_date = models.DateTimeField(null=True, blank=True)
    
    # Status and timestamps
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['crypto_index', 'status']),
            models.Index(fields=['cryptocurrency', 'status']),
        ]
    
    def __str__(self):
        target = self.crypto_index.name if self.crypto_index else self.cryptocurrency.name
        return f"{self.user.email} - {self.name} ({target})"
    
    @property
    def total_return_percent(self):
        """Calculate total return percentage"""
        if self.total_invested_btc and self.total_invested_btc > 0:
            return ((self.current_value_btc - self.total_invested_btc) / self.total_invested_btc) * 100
        return 0
    
    @property
    def is_profitable(self):
        """Check if investment is currently profitable"""
        return self.unrealized_pnl_btc > 0
    
    @property
    def investment_target_name(self):
        """Get the name of what user is investing in"""
        if self.crypto_index:
            return self.crypto_index.name
        elif self.cryptocurrency:
            return self.cryptocurrency.name
        return "Unknown"


class InvestmentTransaction(models.Model):
    """Track individual transactions within an investment"""
    
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit/Add Funds'),
        ('withdraw', 'Withdraw/Reduce Position'),
        ('compound', 'Compound Gains'),
        ('rebalance', 'Portfolio Rebalance'),
        ('dividend', 'Dividend/Reward Payment'),
        ('fee', 'Management Fee'),
    ]
    
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    
    # Transaction details
    amount_btc = models.DecimalField(max_digits=20, decimal_places=8)
    amount_usd = models.DecimalField(max_digits=20, decimal_places=2)
    btc_price_at_transaction = models.DecimalField(max_digits=20, decimal_places=8)
    
    # Index value at transaction time (for index investments)
    index_value_at_transaction = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    
    # Fees and metadata
    fees_btc = models.DecimalField(max_digits=10, decimal_places=8, default=0)
    notes = models.TextField(blank=True)
    is_automatic = models.BooleanField(default=False)  # For DCA or auto-compound
    
    transaction_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-transaction_date']
    
    def __str__(self):
        return f"{self.investment.name} - {self.transaction_type} {self.amount_btc} BTC"
