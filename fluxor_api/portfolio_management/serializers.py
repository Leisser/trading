"""
Portfolio Management Serializers
"""
from rest_framework import serializers
from .models import Portfolio, PortfolioBalance, Transaction, PnLRecord, AssetAllocation


class PortfolioSerializer(serializers.ModelSerializer):
    """Serializer for Portfolio model"""
    
    class Meta:
        model = Portfolio
        fields = [
            'id', 'name', 'description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PortfolioBalanceSerializer(serializers.ModelSerializer):
    """Serializer for PortfolioBalance model"""
    
    class Meta:
        model = PortfolioBalance
        fields = [
            'id', 'portfolio', 'symbol', 'balance', 'current_value', 
            'average_cost', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'portfolio', 'transaction_type', 'symbol', 'amount', 
            'price', 'value', 'fees', 'notes', 'transaction_date'
        ]
        read_only_fields = ['id', 'transaction_date']


class PnLRecordSerializer(serializers.ModelSerializer):
    """Serializer for PnLRecord model"""
    
    class Meta:
        model = PnLRecord
        fields = [
            'id', 'portfolio', 'date', 'total_pnl', 'realized_pnl', 'unrealized_pnl',
            'total_return', 'daily_return', 'max_drawdown', 'volatility', 
            'sharpe_ratio', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AssetAllocationSerializer(serializers.ModelSerializer):
    """Serializer for AssetAllocation model"""
    
    class Meta:
        model = AssetAllocation
        fields = [
            'id', 'portfolio', 'symbol', 'allocation_percentage', 
            'target_allocation', 'current_value', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


class PortfolioSummarySerializer(serializers.Serializer):
    """Serializer for portfolio summary data"""
    
    portfolio_id = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_pnl = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_pnl_percentage = serializers.DecimalField(max_digits=10, decimal_places=4)
    total_transactions = serializers.IntegerField()
    total_deposits = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_withdrawals = serializers.DecimalField(max_digits=20, decimal_places=2)
    asset_count = serializers.IntegerField()


class PerformanceAnalyticsSerializer(serializers.Serializer):
    """Serializer for performance analytics data"""
    
    period = serializers.CharField()
    total_return = serializers.DecimalField(max_digits=10, decimal_places=4)
    annualized_return = serializers.DecimalField(max_digits=10, decimal_places=4)
    volatility = serializers.DecimalField(max_digits=10, decimal_places=4)
    sharpe_ratio = serializers.DecimalField(max_digits=10, decimal_places=4)
    max_drawdown = serializers.DecimalField(max_digits=10, decimal_places=4)
    win_rate = serializers.DecimalField(max_digits=5, decimal_places=2)


class RiskMetricsSerializer(serializers.Serializer):
    """Serializer for risk metrics data"""
    
    value_at_risk = serializers.DecimalField(max_digits=10, decimal_places=4)
    expected_shortfall = serializers.DecimalField(max_digits=10, decimal_places=4)
    beta = serializers.DecimalField(max_digits=10, decimal_places=4)
    correlation_matrix = serializers.JSONField()
    diversification_ratio = serializers.DecimalField(max_digits=10, decimal_places=4)
