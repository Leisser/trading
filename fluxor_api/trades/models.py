from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid

User = settings.AUTH_USER_MODEL


class Cryptocurrency(models.Model):
    """Enhanced Cryptocurrency model for comprehensive crypto data"""
    
    # Basic Information
    symbol = models.CharField(max_length=20, unique=True)  # Increased for longer symbols
    name = models.CharField(max_length=200)  # Increased for longer names
    coin_id = models.CharField(max_length=100, blank=True)  # For API identification
    rank = models.PositiveIntegerField(default=999, db_index=True)  # Market cap rank
    
    # Pricing Data
    current_price = models.DecimalField(max_digits=30, decimal_places=12, default=0)
    market_cap = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    volume_24h = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    
    # Supply Information
    circulating_supply = models.DecimalField(max_digits=30, decimal_places=8, default=0)
    total_supply = models.DecimalField(max_digits=30, decimal_places=8, default=0, null=True, blank=True)
    max_supply = models.DecimalField(max_digits=30, decimal_places=8, default=0, null=True, blank=True)
    
    # Price Changes (percentage)
    price_change_1h = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    price_change_24h = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    price_change_7d = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    price_change_30d = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    price_change_1y = models.DecimalField(max_digits=10, decimal_places=4, default=0, null=True, blank=True)
    
    # Trading Metrics
    volume_change_24h = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    market_cap_change_24h = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    # Technical Indicators (updated by trading algorithms)
    rsi_14 = models.DecimalField(max_digits=5, decimal_places=2, default=50, null=True, blank=True)
    ma_20 = models.DecimalField(max_digits=30, decimal_places=12, default=0, null=True, blank=True)
    ma_50 = models.DecimalField(max_digits=30, decimal_places=12, default=0, null=True, blank=True)
    
    # Blockchain Information
    blockchain_network = models.CharField(max_length=50, blank=True)  # e.g., "Ethereum", "Binance Smart Chain"
    contract_address = models.CharField(max_length=255, blank=True)  # For tokens
    decimals = models.PositiveIntegerField(default=18, null=True, blank=True)  # Token decimals
    
    # Categories and Tags
    categories = models.JSONField(default=list, blank=True)  # ["DeFi", "Layer 1", etc.]
    tags = models.JSONField(default=list, blank=True)  # More specific tags
    
    # Status and Control
    is_active = models.BooleanField(default=True)
    is_tradeable = models.BooleanField(default=True)
    is_stablecoin = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)  # For highlighting popular coins
    
    # Data Sources
    data_source = models.CharField(max_length=50, default='coinmarketcap')  # API source
    last_updated_external = models.DateTimeField(null=True, blank=True)  # When external data was updated
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('cryptocurrency')
        verbose_name_plural = _('cryptocurrencies')
    
    def __str__(self):
        return f"{self.symbol} - {self.name}"


class CryptoWallet(models.Model):
    """Crypto wallet model for different cryptocurrencies"""
    
    WALLET_TYPE_CHOICES = [
        ('bitcoin', 'Bitcoin'),
        ('ethereum', 'Ethereum'),
        ('solana', 'Solana'),
        ('cardano', 'Cardano'),
        ('polkadot', 'Polkadot'),
        ('chainlink', 'Chainlink'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crypto_wallets')
    wallet_type = models.CharField(max_length=20, choices=WALLET_TYPE_CHOICES)
    address = models.CharField(max_length=255, unique=True)
    private_key_encrypted = models.TextField(blank=True)  # Encrypted private key
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    label = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'wallet_type']
    
    def __str__(self):
        return f"{self.user.email} - {self.wallet_type} ({self.address})"


class Wallet(models.Model):
    """User wallet model (legacy - keeping for compatibility)"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    address = models.CharField(max_length=255, unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    label = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.address}"


class Trade(models.Model):
    """Enhanced Trade model"""
    
    TRADE_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('swap', 'Swap'),  # New: Crypto-to-crypto swap
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('executed', 'Executed'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, null=True, blank=True)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    total_value = models.DecimalField(max_digits=20, decimal_places=2)
    leverage = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    pnl = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    fees = models.DecimalField(max_digits=10, decimal_places=8, default=0)
    executed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Legacy fields for backward compatibility
    btc_amount = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    usd_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if self.cryptocurrency:
            return f"{self.user.email} - {self.trade_type} {self.amount} {self.cryptocurrency.symbol}"
        else:
            return f"{self.user.email} {self.trade_type} {self.btc_amount} BTC @ {self.usd_price} USD"
    
    def save(self, *args, **kwargs):
        if not self.total_value:
            if self.price and self.amount:
                self.total_value = self.amount * self.price
        super().save(*args, **kwargs)


class CryptoSwap(models.Model):
    """Crypto-to-crypto swap model"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crypto_swaps')
    from_cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, related_name='swaps_from')
    to_cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, related_name='swaps_to')
    from_amount = models.DecimalField(max_digits=20, decimal_places=8)
    to_amount = models.DecimalField(max_digits=20, decimal_places=8)
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=8)
    network_fee = models.DecimalField(max_digits=10, decimal_places=8, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_hash = models.CharField(max_length=255, blank=True)
    swap_provider = models.CharField(max_length=50, default='1inch')  # 1inch, uniswap, etc.
    executed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.from_amount} {self.from_cryptocurrency.symbol} → {self.to_amount} {self.to_cryptocurrency.symbol}"


class PriceData(models.Model):
    """Historical price data"""
    
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=20, decimal_places=2)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField()
    source = models.CharField(max_length=50, default='binance')  # binance, coingecko, etc.
    
    class Meta:
        ordering = ['-timestamp']
        unique_together = ['cryptocurrency', 'timestamp', 'source']
    
    def __str__(self):
        return f"{self.cryptocurrency.symbol} - {self.price} at {self.timestamp}"


class TradingSignal(models.Model):
    """Trading signals"""
    
    SIGNAL_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('hold', 'Hold'),
    ]
    
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    signal_type = models.CharField(max_length=4, choices=SIGNAL_TYPE_CHOICES)
    confidence = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100
    price_target = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    reasoning = models.TextField(blank=True)
    indicators = models.JSONField(default=dict)  # RSI, MACD, etc.
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.cryptocurrency.symbol} - {self.signal_type} ({self.confidence}%)"


class Deposit(models.Model):
    """Deposit model"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    transaction_hash = models.CharField(max_length=255, blank=True)
    wallet_address = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.cryptocurrency.symbol}"


class Withdrawal(models.Model):
    """Withdrawal model"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    to_address = models.CharField(max_length=255)
    transaction_hash = models.CharField(max_length=255, blank=True)
    fees = models.DecimalField(max_digits=10, decimal_places=8, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.cryptocurrency.symbol} to {self.to_address}"


class CryptoPayment(models.Model):
    """Crypto payment model for accepting payments"""
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('expired', 'Expired'),
        ('failed', 'Failed'),
    ]
    
    PAYMENT_PROVIDER_CHOICES = [
        ('coinbase', 'Coinbase Commerce'),
        ('nowpayments', 'NOWPayments'),
        ('bitpay', 'BitPay'),
        ('btcpay', 'BTCPay Server'),
    ]
    
    payment_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crypto_payments')
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    amount_crypto = models.DecimalField(max_digits=20, decimal_places=8)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    payment_provider = models.CharField(max_length=20, choices=PAYMENT_PROVIDER_CHOICES)
    provider_payment_id = models.CharField(max_length=255, blank=True)
    payment_url = models.URLField(blank=True)
    wallet_address = models.CharField(max_length=255)
    transaction_hash = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    expires_at = models.DateTimeField()
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.amount_usd} USD ({self.amount_crypto} {self.cryptocurrency.symbol})"


class CryptoIndex(models.Model):
    """Cryptocurrency index model for index investing"""
    
    INDEX_TYPES = [
        ('market_cap', 'Market Cap Weighted'),
        ('equal_weight', 'Equal Weighted'),
        ('custom', 'Custom Weighted'),
        ('defi', 'DeFi Index'),
        ('layer1', 'Layer 1 Index'),
        ('metaverse', 'Metaverse Index'),
        ('gamefi', 'GameFi Index'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=20, unique=True)  # e.g., "BTC10" for top 10 crypto index
    description = models.TextField()
    index_type = models.CharField(max_length=15, choices=INDEX_TYPES, default='market_cap')
    
    # Index composition
    cryptocurrencies = models.ManyToManyField(Cryptocurrency, through='IndexComponent')
    
    # Index performance
    current_value = models.DecimalField(max_digits=20, decimal_places=8, default=1000)  # Base value of 1000
    total_market_cap = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    price_change_24h = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    price_change_7d = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    price_change_30d = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    # Index settings
    is_active = models.BooleanField(default=True)
    is_tradeable = models.BooleanField(default=True)
    minimum_investment = models.DecimalField(max_digits=20, decimal_places=8, default=0.001)  # In BTC
    management_fee = models.DecimalField(max_digits=5, decimal_places=4, default=0)  # Annual fee %
    
    # Rebalancing
    rebalance_frequency = models.CharField(max_length=10, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ], default='monthly')
    last_rebalanced = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.symbol})"
    
    @property
    def total_components(self):
        """Get total number of cryptocurrencies in index"""
        return self.components.count()
    
    @property
    def performance_ytd(self):
        """Calculate year-to-date performance"""
        # This would calculate based on historical data
        return 0  # Placeholder


class IndexComponent(models.Model):
    """Components of a crypto index with their weights"""
    
    crypto_index = models.ForeignKey(CryptoIndex, on_delete=models.CASCADE, related_name='components')
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    
    # Weight settings
    weight_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100%
    target_weight = models.DecimalField(max_digits=5, decimal_places=2)  # Target allocation
    current_weight = models.DecimalField(max_digits=5, decimal_places=2)  # Current actual weight
    
    # Performance contribution
    contribution_to_return = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['crypto_index', 'cryptocurrency']
        ordering = ['-weight_percentage']
    
    def __str__(self):
        return f"{self.crypto_index.symbol} - {self.cryptocurrency.symbol} ({self.weight_percentage}%)"


class CryptoInvestment(models.Model):
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crypto_investments')
    investment_type = models.CharField(max_length=15, choices=INVESTMENT_TYPES, default='index')
    
    # Investment target (either index or single crypto)
    crypto_index = models.ForeignKey(CryptoIndex, on_delete=models.CASCADE, null=True, blank=True, related_name='investments')
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, null=True, blank=True, related_name='single_investments')
    
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
    """Track individual transactions within a crypto investment"""
    
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit/Add Funds'),
        ('withdraw', 'Withdraw/Reduce Position'),
        ('compound', 'Compound Gains'),
        ('rebalance', 'Portfolio Rebalance'),
        ('dividend', 'Dividend/Reward Payment'),
        ('fee', 'Management Fee'),
    ]
    
    investment = models.ForeignKey(CryptoInvestment, on_delete=models.CASCADE, related_name='transactions')
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


class IndexPriceHistory(models.Model):
    """Historical price data for crypto indices"""
    
    crypto_index = models.ForeignKey(CryptoIndex, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=20, decimal_places=8)
    market_cap = models.DecimalField(max_digits=30, decimal_places=2)
    volume_24h = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    
    # Daily performance
    daily_return = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    cumulative_return = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    timestamp = models.DateTimeField()
    
    class Meta:
        unique_together = ['crypto_index', 'timestamp']
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['crypto_index', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.crypto_index.symbol} - {self.price} at {self.timestamp}"


# Admin Settings and Control Models
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
    trading_fee_percentage = models.DecimalField(max_digits=5, decimal_places=4, default=0.1)
    investment_management_fee = models.DecimalField(max_digits=5, decimal_places=4, default=0.5)
    withdrawal_fee_percentage = models.DecimalField(max_digits=5, decimal_places=4, default=0.05)
    
    # Auto-trading Settings
    enable_auto_trading = models.BooleanField(default=False)
    auto_trade_frequency = models.IntegerField(default=60)  # Every 60 seconds
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Trading Settings'
        verbose_name_plural = 'Trading Settings'
    
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
    scenario_type = models.CharField(max_length=10, choices=SCENARIO_TYPES)
    
    # Profit/Loss Parameters
    percentage_change = models.DecimalField(max_digits=10, decimal_places=4)  # +100 for 100% profit, -50 for 50% loss
    time_duration = models.IntegerField()  # Duration value
    time_unit = models.CharField(max_length=10, choices=TIME_UNITS)
    
    # Target Settings
    target_crypto_index = models.ForeignKey(CryptoIndex, on_delete=models.CASCADE, null=True, blank=True)
    target_cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, null=True, blank=True)
    apply_to_all_investments = models.BooleanField(default=False)
    
    # Execution Settings
    is_active = models.BooleanField(default=False)
    execute_immediately = models.BooleanField(default=False)
    scheduled_execution = models.DateTimeField(null=True, blank=True)
    
    # Tracking
    times_executed = models.IntegerField(default=0)
    last_executed = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_scenarios')
    
    class Meta:
        ordering = ['-created_at']
    
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
            'months': 2628000,  # Average month
        }
        return self.time_duration * multipliers.get(self.time_unit, 1)


class DepositWallet(models.Model):
    """System deposit wallets for different cryptocurrencies"""
    
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=255, unique=True)
    wallet_name = models.CharField(max_length=100)  # e.g., "Main Bitcoin Wallet", "Backup ETH Wallet"
    
    # Wallet Status
    is_active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)  # Primary wallet for this crypto
    
    # Balance Tracking
    current_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    total_received = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    total_confirmed = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    
    # Settings
    min_confirmation_blocks = models.IntegerField(default=3)
    auto_confirm_threshold = models.DecimalField(max_digits=20, decimal_places=8, default=0)  # 0 = no auto-confirm
    
    # Metadata
    private_key_encrypted = models.TextField(blank=True)  # Encrypted private key
    wallet_provider = models.CharField(max_length=50, blank=True)  # "coinbase", "binance", "custom"
    api_credentials = models.JSONField(default=dict)  # Store encrypted API keys if needed
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_wallets')
    
    class Meta:
        unique_together = ['cryptocurrency', 'is_primary']
        ordering = ['-is_primary', 'cryptocurrency__symbol']
    
    def __str__(self):
        primary = " (Primary)" if self.is_primary else ""
        return f"{self.wallet_name} - {self.cryptocurrency.symbol}{primary}"


class UserDepositRequest(models.Model):
    """User deposit requests with pending/confirmed status"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposit_requests')
    deposit_wallet = models.ForeignKey(DepositWallet, on_delete=models.CASCADE)
    
    # Deposit Details
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    transaction_hash = models.CharField(max_length=255, blank=True)
    from_address = models.CharField(max_length=255, blank=True)  # User's wallet address
    
    # Status and Confirmation
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    confirmation_blocks = models.IntegerField(default=0)
    required_confirmations = models.IntegerField(default=3)
    
    # Admin Review
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_deposits')
    review_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)  # Auto-expire after 24 hours
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.deposit_wallet.cryptocurrency.symbol} ({self.status})"
    
    def can_be_edited(self):
        """Check if deposit request can still be edited"""
        return self.status == 'pending' and not self.reviewed_by
    
    def is_expired(self):
        """Check if deposit request has expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class PriceMovementLog(models.Model):
    """Log all price movements for detailed tracking"""
    
    # Target
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, null=True, blank=True)
    crypto_index = models.ForeignKey(CryptoIndex, on_delete=models.CASCADE, null=True, blank=True)
    
    # Price Data
    previous_price = models.DecimalField(max_digits=20, decimal_places=8)
    new_price = models.DecimalField(max_digits=20, decimal_places=8)
    price_change = models.DecimalField(max_digits=20, decimal_places=8)
    price_change_percent = models.DecimalField(max_digits=10, decimal_places=4)
    
    # Movement Details
    movement_type = models.CharField(max_length=20, choices=[
        ('natural', 'Natural Market Movement'),
        ('admin_controlled', 'Admin Controlled'),
        ('scenario_based', 'Scenario Execution'),
        ('auto_trading', 'Auto Trading'),
    ], default='natural')
    
    # Source Information
    triggered_by_scenario = models.ForeignKey(ProfitLossScenario, on_delete=models.SET_NULL, null=True, blank=True)
    triggered_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    volume_affected = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['cryptocurrency', 'timestamp']),
            models.Index(fields=['crypto_index', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        target = self.cryptocurrency or self.crypto_index
        return f"{target} - {self.price_change_percent}% at {self.timestamp}"


class AutomatedTask(models.Model):
    """Track automated background tasks"""
    
    TASK_TYPES = [
        ('price_update', 'Price Update'),
        ('investment_calculation', 'Investment Calculation'),
        ('portfolio_update', 'Portfolio Update'),
        ('scenario_execution', 'Scenario Execution'),
        ('deposit_check', 'Deposit Check'),
        ('notification_send', 'Notification Send'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    task_type = models.CharField(max_length=25, choices=TASK_TYPES)
    task_name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Execution Details
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    # Results
    items_processed = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    error_messages = models.TextField(blank=True)
    
    # Metadata
    task_data = models.JSONField(default=dict)  # Store task-specific data
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['task_type', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.task_name} - {self.status} ({self.created_at})"


class Notification(models.Model):
    """User notifications"""
    
    TYPE_CHOICES = [
        ('trade', 'Trade'),
        ('swap', 'Crypto Swap'),
        ('payment', 'Payment'),
        ('price', 'Price Alert'),
        ('signal', 'Trading Signal'),
        ('investment', 'Investment Update'),
        ('rebalance', 'Index Rebalance'),
        ('dca', 'DCA Transaction'),
        ('deposit', 'Deposit Update'),
        ('withdrawal', 'Withdrawal'),
        ('system', 'System'),
        ('security', 'Security'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_notifications')
    notification_type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    data = models.JSONField(default=dict)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
