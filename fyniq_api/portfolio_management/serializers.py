"""
Serializers for Portfolio Management API.
"""
from rest_framework import serializers
from decimal import Decimal
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
    unrealized_pnl = serializers.SerializerMethodField()
    unrealized_pnl_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = PortfolioBalance
        fields = [
            'id', 'asset', 'quantity', 'current_price', 'current_value',
            'average_cost', 'unrealized_pnl', 'unrealized_pnl_percentage',
            'last_updated'
        ]
        read_only_fields = ['id', 'unrealized_pnl', 'unrealized_pnl_percentage', 'last_updated']
    
    def get_unrealized_pnl(self, obj):
        """Calculate unrealized P&L"""
        if obj.quantity > 0 and obj.average_cost > 0:
            return obj.current_value - (obj.quantity * obj.average_cost)
        return Decimal('0')
    
    def get_unrealized_pnl_percentage(self, obj):
        """Calculate unrealized P&L percentage"""
        if obj.quantity > 0 and obj.average_cost > 0:
            cost_basis = obj.quantity * obj.average_cost
            pnl = obj.current_value - cost_basis
            return (pnl / cost_basis) * 100
        return 0

class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'asset', 'quantity', 'price', 'total_value',
            'fees', 'timestamp', 'notes', 'exchange', 'transaction_id'
        ]
        read_only_fields = ['id', 'timestamp']
    
    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be positive")
        return value
    
    def validate_price(self, value):
        """Validate price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value

class PnLRecordSerializer(serializers.ModelSerializer):
    """Serializer for PnLRecord model"""
    class Meta:
        model = PnLRecord
        fields = [
            'id', 'date', 'total_value', 'total_pnl', 'daily_pnl',
            'pnl_percentage', 'realized_pnl', 'unrealized_pnl'
        ]
        read_only_fields = ['id']

class AssetAllocationSerializer(serializers.Serializer):
    """Serializer for asset allocation data"""
    asset = serializers.CharField()
    value = serializers.DecimalField(max_digits=20, decimal_places=8)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    quantity = serializers.DecimalField(max_digits=20, decimal_places=8)
    current_price = serializers.DecimalField(max_digits=20, decimal_places=8)

class PortfolioSummarySerializer(serializers.Serializer):
    """Serializer for portfolio summary"""
    portfolio_id = serializers.IntegerField()
    portfolio_name = serializers.CharField()
    total_value = serializers.DecimalField(max_digits=20, decimal_places=8)
    total_pnl = serializers.DecimalField(max_digits=20, decimal_places=8)
    total_pnl_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    currency = serializers.CharField()
    total_assets = serializers.IntegerField()
    total_transactions = serializers.IntegerField()
    total_deposits = serializers.DecimalField(max_digits=20, decimal_places=8)
    total_withdrawals = serializers.DecimalField(max_digits=20, decimal_places=8)
    net_deposits = serializers.DecimalField(max_digits=20, decimal_places=8)
    last_updated = serializers.DateTimeField()

class PerformanceAnalyticsSerializer(serializers.Serializer):
    """Serializer for performance analytics"""
    period = serializers.CharField()
    total_pnl = serializers.DecimalField(max_digits=20, decimal_places=8)
    total_pnl_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    daily_pnl_avg = serializers.DecimalField(max_digits=20, decimal_places=8)
    best_day = serializers.DictField(allow_null=True)
    worst_day = serializers.DictField(allow_null=True)
    volatility = serializers.DecimalField(max_digits=10, decimal_places=6)
    sharpe_ratio = serializers.DecimalField(max_digits=10, decimal_places=6)
    total_days = serializers.IntegerField()

class RiskMetricsSerializer(serializers.Serializer):
    """Serializer for risk metrics"""
    period = serializers.CharField()
    value_at_risk_95 = serializers.DecimalField(max_digits=10, decimal_places=6)
    value_at_risk_99 = serializers.DecimalField(max_digits=10, decimal_places=6)
    max_drawdown = serializers.DecimalField(max_digits=5, decimal_places=4)
    volatility = serializers.DecimalField(max_digits=10, decimal_places=6)
    beta = serializers.DecimalField(max_digits=5, decimal_places=2)
    sharpe_ratio = serializers.DecimalField(max_digits=10, decimal_places=6)
    total_observations = serializers.IntegerField()

class RebalanceRequestSerializer(serializers.Serializer):
    """Serializer for rebalance requests"""
    portfolio_id = serializers.IntegerField(required=False)
    target_allocation = serializers.DictField(
        child=serializers.DecimalField(max_digits=5, decimal_places=2)
    )
    
    def validate_target_allocation(self, value):
        """Validate that allocation percentages sum to 100"""
        total = sum(value.values())
        if abs(total - 100) > 0.01:  # Allow small floating point errors
            raise serializers.ValidationError("Allocation percentages must sum to 100%")
        return value

class PortfolioHistorySerializer(serializers.Serializer):
    """Serializer for portfolio history"""
    date = serializers.DateField()
    total_value = serializers.DecimalField(max_digits=20, decimal_places=8)
    total_pnl = serializers.DecimalField(max_digits=20, decimal_places=8)
    daily_pnl = serializers.DecimalField(max_digits=20, decimal_places=8)
    pnl_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
