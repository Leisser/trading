from rest_framework import serializers
from .models import (
    Trade, Cryptocurrency, CryptoWallet, CryptoSwap, PriceData, 
    TradingSignal, Deposit, Withdrawal, CryptoPayment, Notification, Wallet,
    CryptoIndex, IndexComponent, CryptoInvestment, InvestmentTransaction, IndexPriceHistory,
    TradingSettings, ProfitLossScenario, DepositWallet, UserDepositRequest,
    PriceMovementLog, AutomatedTask
)
from decimal import Decimal

class TradeSerializer(serializers.ModelSerializer):
    """
    Serializer for trade creation and retrieval.
    
    Example Request:
    {
        "trade_type": "buy",
        "btc_amount": "0.001",
        "usd_price": "45000.00"
    }
    
    Example Response:
    {
        "id": 1,
        "user": 1,
        "trade_type": "buy",
        "btc_amount": "0.001",
        "usd_price": "45000.00",
        "status": "completed",
        "timestamp": "2024-01-01T12:00:00Z",
        "total_value": "45.00"
    }
    """
    total_value = serializers.SerializerMethodField()
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Trade
        fields = [
            'id', 'user', 'user_email', 'trade_type', 'btc_amount', 
            'usd_price', 'status', 'timestamp', 'total_value'
        ]
        read_only_fields = ['id', 'user', 'status', 'timestamp', 'total_value']
    
    def get_total_value(self, obj):
        """Calculate total value of the trade in USD."""
        try:
            btc_amount = Decimal(str(obj.btc_amount))
            usd_price = Decimal(str(obj.usd_price))
            return float(btc_amount * usd_price)
        except (ValueError, TypeError):
            return 0.0
    
    def validate_btc_amount(self, value):
        """Validate BTC amount is positive and reasonable."""
        try:
            amount = Decimal(str(value))
            if amount <= 0:
                raise serializers.ValidationError("BTC amount must be positive")
            if amount > 100:  # Max 100 BTC per trade
                raise serializers.ValidationError("BTC amount cannot exceed 100")
            return value
        except (ValueError, TypeError):
            raise serializers.ValidationError("Invalid BTC amount")
    
    def validate_usd_price(self, value):
        """Validate USD price is positive and reasonable."""
        try:
            price = Decimal(str(value))
            if price <= 0:
                raise serializers.ValidationError("USD price must be positive")
            if price > 1000000:  # Max $1M per BTC
                raise serializers.ValidationError("USD price seems unrealistic")
            return value
        except (ValueError, TypeError):
            raise serializers.ValidationError("Invalid USD price")

class AdvancedTradeSerializer(serializers.Serializer):
    """
    Serializer for advanced trading with leverage and risk management.
    
    Example Request:
    {
        "trade_type": "buy",
        "amount": 1000.00,
        "leverage": 2.0
    }
    
    Example Response:
    {
        "status": "Trade executed (simulated)",
        "trade_id": 123,
        "executed_price": 45000.00,
        "btc_amount": "0.04444444",
        "leverage_used": 2.0,
        "risk_check": "passed",
        "compliance_check": "passed"
    }
    """
    trade_type = serializers.ChoiceField(
        choices=[('buy', 'Buy'), ('sell', 'Sell')],
        help_text="Type of trade to execute"
    )
    amount = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        min_value=10.0,
        max_value=100000.0,
        help_text="Amount in USD (min: $10, max: $100,000)"
    )
    leverage = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        min_value=1.0,
        max_value=10.0,
        help_text="Leverage multiplier (1.0x to 10.0x)"
    )

class TradeHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for trade history with additional calculated fields.
    
    Example Response:
    {
        "count": 25,
        "next": "http://localhost:8000/api/trades/?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "trade_type": "buy",
                "btc_amount": "0.001",
                "usd_price": "45000.00",
                "status": "completed",
                "timestamp": "2024-01-01T12:00:00Z",
                "pnl": 150.00,
                "roi": 3.33
            }
        ]
    }
    """
    pnl = serializers.SerializerMethodField(help_text="Profit/Loss in USD")
    roi = serializers.SerializerMethodField(help_text="Return on Investment percentage")
    
    class Meta:
        model = Trade
        fields = [
            'id', 'trade_type', 'btc_amount', 'usd_price', 'status', 
            'timestamp', 'pnl', 'roi'
        ]
    
    def get_pnl(self, obj):
        """Calculate P&L for the trade (mock data for demonstration)."""
        import random
        return round(random.uniform(-500, 500), 2)
    
    def get_roi(self, obj):
        """Calculate ROI for the trade (mock data for demonstration)."""
        import random
        return round(random.uniform(-10, 10), 2)

class WithdrawalSerializer(serializers.Serializer):
    """
    Serializer for withdrawal requests.
    
    Example Request:
    {
        "amount": "0.001",
        "to_address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
    }
    
    Example Response:
    {
        "status": "Withdrawal request submitted",
        "withdrawal_id": "W123456789",
        "amount": "0.001",
        "to_address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
        "fee": "0.0001",
        "estimated_arrival": "2024-01-01T18:00:00Z"
    }
    """
    amount = serializers.CharField(
        help_text="Amount in BTC to withdraw"
    )
    to_address = serializers.CharField(
        help_text="Bitcoin address to send funds to"
    )
    
    def validate_amount(self, value):
        """Validate withdrawal amount."""
        try:
            amount = Decimal(value)
            if amount <= 0:
                raise serializers.ValidationError("Amount must be positive")
            if amount < 0.0001:  # Min withdrawal 0.0001 BTC
                raise serializers.ValidationError("Minimum withdrawal is 0.0001 BTC")
            if amount > 10:  # Max withdrawal 10 BTC
                raise serializers.ValidationError("Maximum withdrawal is 10 BTC")
            return value
        except (ValueError, TypeError):
            raise serializers.ValidationError("Invalid amount")
    
    def validate_to_address(self, value):
        """Basic Bitcoin address validation."""
        if not value.startswith(('1', '3', 'bc1')):
            raise serializers.ValidationError("Invalid Bitcoin address format")
        if len(value) < 26 or len(value) > 90:
            raise serializers.ValidationError("Invalid Bitcoin address length")
        return value

class DepositCheckSerializer(serializers.Serializer):
    """
    Serializer for deposit check responses.
    
    Example Response:
    {
        "status": "Deposits checked",
        "new_deposits": [
            {
                "txid": "abc123...",
                "amount": "0.005",
                "confirmations": 6,
                "timestamp": "2024-01-01T12:00:00Z"
            }
        ],
        "wallet_balance": "0.125",
        "last_checked": "2024-01-01T12:05:00Z"
    }
    """
    status = serializers.CharField(help_text="Status of the deposit check")
    new_deposits = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of new deposits found"
    )
    wallet_balance = serializers.CharField(help_text="Current wallet balance in BTC")
    last_checked = serializers.DateTimeField(help_text="Timestamp of last check")

class TradeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new trades.
    
    Example Request:
    {
        "trade_type": "buy",
        "btc_amount": "0.001",
        "usd_price": "45000.00"
    }
    """
    class Meta:
        model = Trade
        fields = ['trade_type', 'btc_amount', 'usd_price']
    
    def validate_btc_amount(self, value):
        """Validate BTC amount is positive and reasonable."""
        try:
            amount = Decimal(str(value))
            if amount <= 0:
                raise serializers.ValidationError("BTC amount must be positive")
            if amount > 100:  # Max 100 BTC per trade
                raise serializers.ValidationError("BTC amount cannot exceed 100")
            return value
        except (ValueError, TypeError):
            raise serializers.ValidationError("Invalid BTC amount")
    
    def validate_usd_price(self, value):
        """Validate USD price is positive and reasonable."""
        try:
            price = Decimal(str(value))
            if price <= 0:
                raise serializers.ValidationError("USD price must be positive")
            if price > 1000000:  # Max $1M per BTC
                raise serializers.ValidationError("USD price seems unrealistic")
            return value
        except (ValueError, TypeError):
            raise serializers.ValidationError("Invalid USD price")

class TradeStatsSerializer(serializers.Serializer):
    """
    Serializer for trading statistics.
    
    Example Response:
    {
        "total_trades": 150,
        "total_volume": "0.500",
        "total_value": "22500.00",
        "profit_loss": "1250.00",
        "win_rate": 0.65,
        "average_trade_size": "0.003",
        "largest_trade": "0.010",
        "most_active_day": "2024-01-15",
        "buy_trades": 80,
        "sell_trades": 70
    }
    """
    total_trades = serializers.IntegerField(help_text="Total number of trades")
    total_volume = serializers.CharField(help_text="Total trading volume in BTC")
    total_value = serializers.CharField(help_text="Total trading value in USD")
    profit_loss = serializers.CharField(help_text="Total profit/loss in USD")
    win_rate = serializers.FloatField(help_text="Win rate as decimal (0.0 to 1.0)")
    average_trade_size = serializers.CharField(help_text="Average trade size in BTC")
    largest_trade = serializers.CharField(help_text="Largest trade amount in BTC")
    most_active_day = serializers.CharField(help_text="Most active trading day")
    buy_trades = serializers.IntegerField(help_text="Number of buy trades")
    sell_trades = serializers.IntegerField(help_text="Number of sell trades")


# New Enhanced Serializers
class CryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class CryptoWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoWallet
        fields = ['id', 'wallet_type', 'address', 'balance', 'label', 'is_active', 'created_at']
        read_only_fields = ['address', 'balance', 'created_at']


class CryptoSwapSerializer(serializers.ModelSerializer):
    from_cryptocurrency_symbol = serializers.CharField(source='from_cryptocurrency.symbol', read_only=True)
    to_cryptocurrency_symbol = serializers.CharField(source='to_cryptocurrency.symbol', read_only=True)
    
    class Meta:
        model = CryptoSwap
        fields = '__all__'
        read_only_fields = ['user', 'to_amount', 'exchange_rate', 'transaction_hash', 'executed_at', 'created_at']


class PriceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceData
        fields = '__all__'


class TradingSignalSerializer(serializers.ModelSerializer):
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    
    class Meta:
        model = TradingSignal
        fields = '__all__'


class DepositSerializer(serializers.ModelSerializer):
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    
    class Meta:
        model = Deposit
        fields = '__all__'
        read_only_fields = ['user', 'status', 'confirmed_at', 'created_at']


class WithdrawalSerializer(serializers.ModelSerializer):
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    
    class Meta:
        model = Withdrawal
        fields = '__all__'
        read_only_fields = ['user', 'transaction_hash', 'status', 'processed_at', 'created_at']


class CryptoPaymentSerializer(serializers.ModelSerializer):
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    
    class Meta:
        model = CryptoPayment
        fields = '__all__'
        read_only_fields = ['user', 'payment_id', 'provider_payment_id', 'payment_url', 'transaction_hash', 'status', 'confirmed_at', 'created_at']


# Request/Response Serializers
class ExecuteTradeSerializer(serializers.Serializer):
    cryptocurrency_id = serializers.IntegerField()
    trade_type = serializers.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')])
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    leverage = serializers.IntegerField(min_value=1, max_value=10, default=1)


class ExecuteSwapSerializer(serializers.Serializer):
    from_cryptocurrency_id = serializers.IntegerField()
    to_cryptocurrency_id = serializers.IntegerField()
    from_amount = serializers.DecimalField(max_digits=20, decimal_places=8)


class CreatePaymentSerializer(serializers.Serializer):
    amount_usd = serializers.DecimalField(max_digits=10, decimal_places=2)
    cryptocurrency = serializers.CharField(max_length=10)


class PriceFeedSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    price = serializers.DecimalField(max_digits=20, decimal_places=8)
    volume = serializers.DecimalField(max_digits=20, decimal_places=2)
    change_24h = serializers.DecimalField(max_digits=10, decimal_places=2)
    timestamp = serializers.DateTimeField()


class TradingSignalRequestSerializer(serializers.Serializer):
    cryptocurrency_id = serializers.IntegerField()
    signal_type = serializers.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell'), ('hold', 'Hold')])
    confidence = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0, max_value=100)
    price_target = serializers.DecimalField(max_digits=20, decimal_places=8, required=False)
    stop_loss = serializers.DecimalField(max_digits=20, decimal_places=8, required=False)
    reasoning = serializers.CharField(required=False)
    indicators = serializers.JSONField(required=False)


class SwapQuoteSerializer(serializers.Serializer):
    from_token = serializers.CharField()
    to_token = serializers.CharField()
    from_amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    to_amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    exchange_rate = serializers.DecimalField(max_digits=20, decimal_places=8)
    network_fee = serializers.DecimalField(max_digits=10, decimal_places=8)
    provider = serializers.CharField()
    estimated_time = serializers.CharField()


class WalletBalanceSerializer(serializers.Serializer):
    wallet_type = serializers.CharField()
    address = serializers.CharField()
    balance = serializers.DecimalField(max_digits=20, decimal_places=8)
    usd_value = serializers.DecimalField(max_digits=20, decimal_places=2)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


# Crypto Investment Serializers
class CryptocurrencySimpleSerializer(serializers.ModelSerializer):
    """Simple serializer for cryptocurrency data in index components"""
    class Meta:
        model = Cryptocurrency
        fields = ['id', 'symbol', 'name', 'current_price', 'price_change_24h']


class IndexComponentSerializer(serializers.ModelSerializer):
    """Serializer for index components"""
    cryptocurrency = CryptocurrencySimpleSerializer(read_only=True)
    
    class Meta:
        model = IndexComponent
        fields = [
            'id', 'cryptocurrency', 'weight_percentage', 'target_weight', 
            'current_weight', 'contribution_to_return', 'is_active', 'added_at'
        ]


class CryptoIndexSerializer(serializers.ModelSerializer):
    """Serializer for crypto indices"""
    components = IndexComponentSerializer(many=True, read_only=True)
    total_components = serializers.ReadOnlyField()
    performance_ytd = serializers.ReadOnlyField()
    
    class Meta:
        model = CryptoIndex
        fields = [
            'id', 'name', 'symbol', 'description', 'index_type', 'components',
            'current_value', 'total_market_cap', 'price_change_24h', 
            'price_change_7d', 'price_change_30d', 'is_active', 'is_tradeable',
            'minimum_investment', 'management_fee', 'rebalance_frequency',
            'last_rebalanced', 'total_components', 'performance_ytd',
            'created_at', 'updated_at'
        ]


class CryptoIndexListSerializer(serializers.ModelSerializer):
    """Simplified serializer for crypto index listing"""
    total_components = serializers.ReadOnlyField()
    
    class Meta:
        model = CryptoIndex
        fields = [
            'id', 'name', 'symbol', 'description', 'index_type', 
            'current_value', 'price_change_24h', 'price_change_7d', 
            'price_change_30d', 'minimum_investment', 'management_fee',
            'total_components', 'is_active', 'is_tradeable'
        ]


class InvestmentTransactionSerializer(serializers.ModelSerializer):
    """Serializer for investment transactions"""
    
    class Meta:
        model = InvestmentTransaction
        fields = [
            'id', 'transaction_type', 'amount_btc', 'amount_usd',
            'btc_price_at_transaction', 'index_value_at_transaction',
            'fees_btc', 'notes', 'is_automatic', 'transaction_date'
        ]


class CryptoInvestmentSerializer(serializers.ModelSerializer):
    """Serializer for crypto investments"""
    crypto_index = CryptoIndexListSerializer(read_only=True)
    cryptocurrency = CryptocurrencySimpleSerializer(read_only=True)
    transactions = InvestmentTransactionSerializer(many=True, read_only=True)
    total_return_percent = serializers.ReadOnlyField()
    is_profitable = serializers.ReadOnlyField()
    investment_target_name = serializers.ReadOnlyField()
    
    # Allow setting crypto_index_id and cryptocurrency_id for creation
    crypto_index_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    cryptocurrency_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = CryptoInvestment
        fields = [
            'id', 'investment_type', 'crypto_index', 'cryptocurrency',
            'crypto_index_id', 'cryptocurrency_id', 'name', 
            'total_invested_btc', 'total_invested_usd', 'current_value_btc',
            'current_value_usd', 'unrealized_pnl_btc', 'unrealized_pnl_usd',
            'unrealized_pnl_percent', 'all_time_high_value', 'max_drawdown_percent',
            'auto_compound', 'dca_amount_btc', 'dca_frequency', 'next_dca_date',
            'status', 'started_at', 'closed_at', 'last_updated',
            'total_return_percent', 'is_profitable', 'investment_target_name',
            'transactions'
        ]
        read_only_fields = [
            'current_value_btc', 'current_value_usd', 'unrealized_pnl_btc',
            'unrealized_pnl_usd', 'unrealized_pnl_percent', 'all_time_high_value',
            'max_drawdown_percent', 'started_at', 'last_updated'
        ]


class CryptoInvestmentListSerializer(serializers.ModelSerializer):
    """Simplified serializer for investment listing"""
    crypto_index = CryptoIndexListSerializer(read_only=True)
    cryptocurrency = CryptocurrencySimpleSerializer(read_only=True)
    total_return_percent = serializers.ReadOnlyField()
    is_profitable = serializers.ReadOnlyField()
    investment_target_name = serializers.ReadOnlyField()
    
    class Meta:
        model = CryptoInvestment
        fields = [
            'id', 'investment_type', 'crypto_index', 'cryptocurrency', 'name',
            'total_invested_btc', 'current_value_btc', 'unrealized_pnl_btc',
            'unrealized_pnl_percent', 'status', 'started_at', 'total_return_percent',
            'is_profitable', 'investment_target_name'
        ]


class InvestmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new investments"""
    crypto_index_id = serializers.IntegerField(required=False, allow_null=True)
    cryptocurrency_id = serializers.IntegerField(required=False, allow_null=True)
    initial_investment_btc = serializers.DecimalField(
        max_digits=20, decimal_places=8, write_only=True
    )
    
    class Meta:
        model = CryptoInvestment
        fields = [
            'investment_type', 'crypto_index_id', 'cryptocurrency_id', 'name',
            'initial_investment_btc', 'auto_compound', 'dca_amount_btc', 
            'dca_frequency'
        ]
    
    def validate(self, data):
        """Validate investment creation data"""
        if not data.get('crypto_index_id') and not data.get('cryptocurrency_id'):
            raise serializers.ValidationError(
                "Either crypto_index_id or cryptocurrency_id must be provided"
            )
        
        if data.get('crypto_index_id') and data.get('cryptocurrency_id'):
            raise serializers.ValidationError(
                "Cannot invest in both index and single cryptocurrency simultaneously"
            )
        
        if data.get('initial_investment_btc', 0) <= 0:
            raise serializers.ValidationError(
                "Initial investment must be greater than 0"
            )
        
        return data


class TransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating investment transactions"""
    
    class Meta:
        model = InvestmentTransaction
        fields = [
            'transaction_type', 'amount_btc', 'notes'
        ]
    
    def validate_amount_btc(self, value):
        """Validate transaction amount"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value


class IndexPriceHistorySerializer(serializers.ModelSerializer):
    """Serializer for index price history"""
    
    class Meta:
        model = IndexPriceHistory
        fields = [
            'price', 'market_cap', 'volume_24h', 'daily_return',
            'cumulative_return', 'timestamp'
        ]


class InvestmentPerformanceSerializer(serializers.Serializer):
    """Serializer for investment performance analytics"""
    total_invested = serializers.DecimalField(max_digits=20, decimal_places=8)
    current_value = serializers.DecimalField(max_digits=20, decimal_places=8)
    total_return = serializers.DecimalField(max_digits=10, decimal_places=4)
    total_return_percent = serializers.DecimalField(max_digits=10, decimal_places=4)
    unrealized_pnl = serializers.DecimalField(max_digits=20, decimal_places=8)
    all_time_high = serializers.DecimalField(max_digits=20, decimal_places=8)
    max_drawdown = serializers.DecimalField(max_digits=10, decimal_places=4)
    investment_duration_days = serializers.IntegerField()
    average_daily_return = serializers.DecimalField(max_digits=10, decimal_places=6)
    sharpe_ratio = serializers.DecimalField(max_digits=10, decimal_places=4, allow_null=True)
    volatility = serializers.DecimalField(max_digits=10, decimal_places=4, allow_null=True)


class PortfolioAllocationSerializer(serializers.Serializer):
    """Serializer for portfolio allocation breakdown"""
    investment_name = serializers.CharField()
    investment_type = serializers.CharField()
    target_name = serializers.CharField()
    current_value_btc = serializers.DecimalField(max_digits=20, decimal_places=8)
    allocation_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    performance_percent = serializers.DecimalField(max_digits=10, decimal_places=4)
    is_profitable = serializers.BooleanField()


# Admin Control Serializers
class TradingSettingsSerializer(serializers.ModelSerializer):
    """Serializer for trading settings"""
    class Meta:
        model = TradingSettings
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ProfitLossScenarioSerializer(serializers.ModelSerializer):
    """Serializer for profit/loss scenarios"""
    duration_in_seconds = serializers.ReadOnlyField()
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    target_crypto_name = serializers.CharField(source='target_cryptocurrency.name', read_only=True)
    target_index_name = serializers.CharField(source='target_crypto_index.name', read_only=True)
    
    class Meta:
        model = ProfitLossScenario
        fields = [
            'id', 'name', 'scenario_type', 'percentage_change', 'time_duration', 'time_unit',
            'target_crypto_index', 'target_cryptocurrency', 'apply_to_all_investments',
            'is_active', 'execute_immediately', 'scheduled_execution', 'times_executed',
            'last_executed', 'created_at', 'created_by', 'created_by_email',
            'target_crypto_name', 'target_index_name', 'duration_in_seconds'
        ]
        read_only_fields = ['created_at', 'created_by', 'times_executed', 'last_executed']


class DepositWalletSerializer(serializers.ModelSerializer):
    """Serializer for deposit wallets"""
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    cryptocurrency_name = serializers.CharField(source='cryptocurrency.name', read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    
    class Meta:
        model = DepositWallet
        fields = [
            'id', 'cryptocurrency', 'wallet_address', 'wallet_name', 'is_active', 'is_primary',
            'current_balance', 'total_received', 'total_confirmed', 'min_confirmation_blocks',
            'auto_confirm_threshold', 'wallet_provider', 'created_at', 'created_by',
            'cryptocurrency_symbol', 'cryptocurrency_name', 'created_by_email'
        ]
        read_only_fields = ['created_at', 'created_by', 'current_balance', 'total_received', 'total_confirmed']


class UserDepositRequestSerializer(serializers.ModelSerializer):
    """Serializer for user deposit requests"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    wallet_name = serializers.CharField(source='deposit_wallet.wallet_name', read_only=True)
    wallet_address = serializers.CharField(source='deposit_wallet.wallet_address', read_only=True)
    cryptocurrency_symbol = serializers.CharField(source='deposit_wallet.cryptocurrency.symbol', read_only=True)
    reviewed_by_email = serializers.CharField(source='reviewed_by.email', read_only=True)
    can_be_edited = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = UserDepositRequest
        fields = [
            'id', 'user', 'deposit_wallet', 'amount', 'transaction_hash', 'from_address',
            'status', 'confirmation_blocks', 'required_confirmations', 'reviewed_by',
            'review_notes', 'reviewed_at', 'created_at', 'confirmed_at', 'expires_at',
            'user_email', 'wallet_name', 'wallet_address', 'cryptocurrency_symbol',
            'reviewed_by_email', 'can_be_edited', 'is_expired'
        ]
        read_only_fields = [
            'user', 'reviewed_by', 'reviewed_at', 'confirmed_at', 'created_at',
            'confirmation_blocks'
        ]


class PriceMovementLogSerializer(serializers.ModelSerializer):
    """Serializer for price movement logs"""
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    crypto_index_symbol = serializers.CharField(source='crypto_index.symbol', read_only=True)
    scenario_name = serializers.CharField(source='triggered_by_scenario.name', read_only=True)
    triggered_by_email = serializers.CharField(source='triggered_by_user.email', read_only=True)
    
    class Meta:
        model = PriceMovementLog
        fields = [
            'id', 'cryptocurrency', 'crypto_index', 'previous_price', 'new_price',
            'price_change', 'price_change_percent', 'movement_type', 'triggered_by_scenario',
            'triggered_by_user', 'volume_affected', 'notes', 'timestamp',
            'cryptocurrency_symbol', 'crypto_index_symbol', 'scenario_name', 'triggered_by_email'
        ]
        read_only_fields = ['timestamp']


class AutomatedTaskSerializer(serializers.ModelSerializer):
    """Serializer for automated tasks"""
    class Meta:
        model = AutomatedTask
        fields = [
            'id', 'task_type', 'task_name', 'status', 'started_at', 'completed_at',
            'duration_seconds', 'items_processed', 'success_count', 'error_count',
            'error_messages', 'task_data', 'created_at'
        ]
        read_only_fields = ['created_at']


class ManualPriceControlSerializer(serializers.Serializer):
    """Serializer for manual price control requests"""
    cryptocurrency_id = serializers.IntegerField(required=False, allow_null=True)
    crypto_index_id = serializers.IntegerField(required=False, allow_null=True)
    price_change_percent = serializers.DecimalField(max_digits=10, decimal_places=4)
    duration_seconds = serializers.IntegerField(default=1)
    
    def validate(self, data):
        if not data.get('cryptocurrency_id') and not data.get('crypto_index_id'):
            raise serializers.ValidationError(
                "Either cryptocurrency_id or crypto_index_id must be provided"
            )
        return data


class DepositApprovalSerializer(serializers.Serializer):
    """Serializer for deposit approval/rejection"""
    notes = serializers.CharField(required=False, allow_blank=True)
