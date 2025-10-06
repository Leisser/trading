"""
Investment Management Serializers
"""
from rest_framework import serializers
from .models import Investment, InvestmentTransaction
from trades.models import CryptoIndex, Cryptocurrency


class InvestmentSerializer(serializers.ModelSerializer):
    """Serializer for Investment model"""
    
    investment_target_name = serializers.ReadOnlyField()
    total_return_percent = serializers.ReadOnlyField()
    is_profitable = serializers.ReadOnlyField()
    
    class Meta:
        model = Investment
        fields = [
            'id', 'user', 'investment_type', 'crypto_index', 'cryptocurrency',
            'name', 'total_invested_btc', 'total_invested_usd', 'current_value_btc',
            'current_value_usd', 'unrealized_pnl_btc', 'unrealized_pnl_usd',
            'unrealized_pnl_percent', 'all_time_high_value', 'max_drawdown_percent',
            'auto_compound', 'dca_amount_btc', 'dca_frequency', 'next_dca_date',
            'status', 'started_at', 'closed_at', 'last_updated',
            'investment_target_name', 'total_return_percent', 'is_profitable'
        ]
        read_only_fields = ['id', 'user', 'started_at', 'last_updated']


class InvestmentTransactionSerializer(serializers.ModelSerializer):
    """Serializer for InvestmentTransaction model"""
    
    class Meta:
        model = InvestmentTransaction
        fields = [
            'id', 'investment', 'transaction_type', 'amount_btc', 'amount_usd',
            'btc_price_at_transaction', 'index_value_at_transaction', 'fees_btc',
            'notes', 'is_automatic', 'transaction_date'
        ]
        read_only_fields = ['id', 'transaction_date']


class CreateInvestmentSerializer(serializers.ModelSerializer):
    """Serializer for creating new investments"""
    
    class Meta:
        model = Investment
        fields = [
            'investment_type', 'crypto_index', 'cryptocurrency', 'name',
            'total_invested_btc', 'total_invested_usd', 'auto_compound',
            'dca_amount_btc', 'dca_frequency'
        ]
    
    def validate(self, data):
        """Validate investment data"""
        if not data.get('crypto_index') and not data.get('cryptocurrency'):
            raise serializers.ValidationError("Either crypto_index or cryptocurrency must be specified")
        
        if data.get('crypto_index') and data.get('cryptocurrency'):
            raise serializers.ValidationError("Cannot specify both crypto_index and cryptocurrency")
        
        return data


class InvestmentPerformanceSerializer(serializers.Serializer):
    """Serializer for investment performance data"""
    
    investment_id = serializers.IntegerField()
    name = serializers.CharField()
    investment_type = serializers.CharField()
    total_invested_usd = serializers.DecimalField(max_digits=20, decimal_places=2)
    current_value_usd = serializers.DecimalField(max_digits=20, decimal_places=2)
    unrealized_pnl_usd = serializers.DecimalField(max_digits=20, decimal_places=2)
    unrealized_pnl_percent = serializers.DecimalField(max_digits=10, decimal_places=4)
    total_return_percent = serializers.DecimalField(max_digits=10, decimal_places=4)
    is_profitable = serializers.BooleanField()
    started_at = serializers.DateTimeField()
    last_updated = serializers.DateTimeField()


class CryptoIndexSerializer(serializers.ModelSerializer):
    """Serializer for CryptoIndex model"""
    
    class Meta:
        model = CryptoIndex
        fields = [
            'id', 'name', 'symbol', 'description', 'index_type',
            'current_value', 'total_market_cap', 'price_change_24h',
            'price_change_7d', 'price_change_30d', 'is_active',
            'is_tradeable', 'minimum_investment', 'management_fee',
            'rebalance_frequency', 'last_rebalanced', 'created_at'
        ]


class CryptocurrencySerializer(serializers.ModelSerializer):
    """Serializer for Cryptocurrency model"""
    
    class Meta:
        model = Cryptocurrency
        fields = [
            'id', 'name', 'symbol', 'current_price', 'market_cap',
            'volume_24h', 'price_change_24h', 'price_change_7d',
            'price_change_30d', 'is_active', 'is_tradeable',
            'is_stablecoin', 'is_featured', 'created_at'
        ]
