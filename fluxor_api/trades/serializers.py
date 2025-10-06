"""
Serializers for trades app models.
"""
from rest_framework import serializers
from decimal import Decimal
from .models import (
    Cryptocurrency, CryptoWallet, Wallet, Trade, Deposit, Withdrawal,
    CryptoPayment, CryptoIndex, IndexComponent, CryptoInvestment,
    ProfitLossScenario, DepositWallet, UserDepositRequest
)


class CryptocurrencySerializer(serializers.ModelSerializer):
    """Serializer for Cryptocurrency model"""
    
    class Meta:
        model = Cryptocurrency
        fields = [
            'id', 'symbol', 'name', 'coin_id', 'rank', 'current_price',
            'market_cap', 'volume_24h', 'circulating_supply', 'total_supply',
            'max_supply', 'price_change_1h', 'price_change_24h', 'price_change_7d',
            'price_change_30d', 'price_change_1y', 'volume_change_24h',
            'market_cap_change_24h', 'rsi_14', 'ma_20', 'ma_50',
            'blockchain_network', 'contract_address', 'decimals', 'categories',
            'tags', 'is_active', 'is_tradeable', 'is_stablecoin', 'is_featured',
            'data_source', 'last_updated_external', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'last_updated_external'
        ]


class CryptocurrencyListSerializer(serializers.ModelSerializer):
    """Simplified serializer for cryptocurrency lists"""
    
    class Meta:
        model = Cryptocurrency
        fields = [
            'id', 'symbol', 'name', 'rank', 'current_price', 'market_cap',
            'price_change_24h', 'volume_24h', 'is_featured', 'is_stablecoin',
            'categories'
        ]


class CryptocurrencyDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for cryptocurrency with all fields"""
    
    class Meta:
        model = Cryptocurrency
        fields = '__all__'
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'last_updated_external'
        ]


class CryptoWalletSerializer(serializers.ModelSerializer):
    """Serializer for CryptoWallet model"""
    
    class Meta:
        model = CryptoWallet
        fields = [
            'id', 'wallet_type', 'address', 'balance', 'label',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WalletSerializer(serializers.ModelSerializer):
    """Serializer for Wallet model"""
    
    class Meta:
        model = Wallet
        fields = [
            'id', 'address', 'balance', 'label', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TradeSerializer(serializers.ModelSerializer):
    """Serializer for Trade model"""
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    
    class Meta:
        model = Trade
        fields = [
            'id', 'user', 'cryptocurrency', 'cryptocurrency_symbol', 'trade_type',
            'amount', 'price', 'total_value', 'leverage', 'status', 'fees',
            'profit_loss', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'total_value', 'profit_loss', 'created_at', 'updated_at'
        ]


class DepositSerializer(serializers.ModelSerializer):
    """Serializer for Deposit model"""
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    
    class Meta:
        model = Deposit
        fields = [
            'id', 'user', 'cryptocurrency', 'cryptocurrency_symbol', 'amount',
            'transaction_hash', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class WithdrawalSerializer(serializers.ModelSerializer):
    """Serializer for Withdrawal model"""
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    
    class Meta:
        model = Withdrawal
        fields = [
            'id', 'user', 'cryptocurrency', 'cryptocurrency_symbol', 'amount',
            'to_address', 'transaction_hash', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class CryptoPaymentSerializer(serializers.ModelSerializer):
    """Serializer for CryptoPayment model"""
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    
    class Meta:
        model = CryptoPayment
        fields = [
            'id', 'payment_id', 'user', 'amount_usd', 'amount_crypto',
            'cryptocurrency', 'cryptocurrency_symbol', 'payment_provider',
            'provider_payment_id', 'payment_url', 'wallet_address',
            'transaction_hash', 'status', 'expires_at', 'confirmed_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'payment_id', 'user', 'transaction_hash', 'confirmed_at',
            'created_at', 'updated_at'
        ]


class IndexComponentSerializer(serializers.ModelSerializer):
    """Serializer for IndexComponent model"""
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    cryptocurrency_name = serializers.CharField(source='cryptocurrency.name', read_only=True)
    
    class Meta:
        model = IndexComponent
        fields = [
            'id', 'crypto_index', 'cryptocurrency', 'cryptocurrency_symbol',
            'cryptocurrency_name', 'weight_percentage', 'added_at'
        ]
        read_only_fields = ['id', 'added_at']


class CryptoIndexSerializer(serializers.ModelSerializer):
    """Serializer for CryptoIndex model"""
    components = IndexComponentSerializer(many=True, read_only=True)
    
    class Meta:
        model = CryptoIndex
        fields = [
            'id', 'name', 'symbol', 'description', 'index_type',
            'current_value', 'total_market_cap', 'price_change_24h',
            'price_change_7d', 'price_change_30d', 'is_active',
            'is_tradeable', 'minimum_investment', 'management_fee',
            'rebalance_frequency', 'last_rebalanced', 'components',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'current_value', 'total_market_cap', 'last_rebalanced',
            'created_at', 'updated_at'
        ]


class CryptoInvestmentSerializer(serializers.ModelSerializer):
    """Serializer for CryptoInvestment model"""
    crypto_index_name = serializers.CharField(source='crypto_index.name', read_only=True)
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    
    class Meta:
        model = CryptoInvestment
        fields = [
            'id', 'user', 'investment_type', 'crypto_index', 'crypto_index_name',
            'cryptocurrency', 'cryptocurrency_symbol', 'name', 'total_invested_btc',
            'total_invested_usd', 'current_value_btc', 'current_value_usd',
            'unrealized_pnl_btc', 'unrealized_pnl_usd', 'unrealized_pnl_percent',
            'all_time_high_value', 'max_drawdown_percent', 'auto_compound',
            'dca_amount_btc', 'dca_frequency', 'next_dca_date', 'status',
            'started_at', 'closed_at', 'last_updated'
        ]
        read_only_fields = [
            'id', 'user', 'total_invested_btc', 'total_invested_usd',
            'current_value_btc', 'current_value_usd', 'unrealized_pnl_btc',
            'unrealized_pnl_usd', 'unrealized_pnl_percent', 'all_time_high_value',
            'max_drawdown_percent', 'started_at', 'closed_at', 'last_updated'
        ]


class ProfitLossScenarioSerializer(serializers.ModelSerializer):
    """Serializer for ProfitLossScenario model"""
    target_crypto_index_name = serializers.CharField(source='target_crypto_index.name', read_only=True)
    target_cryptocurrency_symbol = serializers.CharField(source='target_cryptocurrency.symbol', read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    
    class Meta:
        model = ProfitLossScenario
        fields = [
            'id', 'name', 'scenario_type', 'percentage_change', 'time_duration',
            'time_unit', 'target_crypto_index', 'target_crypto_index_name',
            'target_cryptocurrency', 'target_cryptocurrency_symbol',
            'apply_to_all_investments', 'apply_to_all_users', 'is_active',
            'execute_immediately', 'scheduled_execution', 'repeat_scenario',
            'repeat_frequency', 'repeat_interval', 'times_executed',
            'last_executed', 'next_execution', 'created_by', 'created_by_email',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'times_executed', 'last_executed', 'next_execution',
            'created_by', 'created_at', 'updated_at'
        ]


class DepositWalletSerializer(serializers.ModelSerializer):
    """Serializer for DepositWallet model"""
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    
    class Meta:
        model = DepositWallet
        fields = [
            'id', 'cryptocurrency', 'cryptocurrency_symbol', 'wallet_address',
            'wallet_name', 'is_active', 'is_primary', 'current_balance',
            'total_received', 'total_confirmed', 'min_confirmation_blocks',
            'auto_confirm_threshold', 'wallet_provider', 'created_by',
            'created_by_email', 'created_at'
        ]
        read_only_fields = [
            'id', 'current_balance', 'total_received', 'total_confirmed',
            'created_by', 'created_at'
        ]


class UserDepositRequestSerializer(serializers.ModelSerializer):
    """Serializer for UserDepositRequest model"""
    cryptocurrency_symbol = serializers.CharField(source='cryptocurrency.symbol', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = UserDepositRequest
        fields = [
            'id', 'user', 'user_email', 'cryptocurrency', 'cryptocurrency_symbol',
            'amount', 'wallet_address', 'transaction_hash', 'status',
            'confirmation_count', 'required_confirmations', 'created_at',
            'confirmed_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'confirmation_count', 'created_at', 'confirmed_at',
            'updated_at'
        ]