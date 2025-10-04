"""
Serializers for Advanced Trading Features.
"""
from rest_framework import serializers
from decimal import Decimal
from .advanced_models import AdvancedOrder, TradingStrategy, OrderExecution, StrategyExecution

class AdvancedOrderSerializer(serializers.ModelSerializer):
    """Serializer for AdvancedOrder model"""
    remaining_quantity = serializers.SerializerMethodField()
    fill_percentage = serializers.SerializerMethodField()
    can_cancel = serializers.SerializerMethodField()
    
    class Meta:
        model = AdvancedOrder
        fields = [
            'id', 'order_type', 'symbol', 'side', 'quantity', 'price', 'stop_price',
            'limit_price', 'time_in_force', 'expire_time', 'trailing_distance',
            'trailing_percentage', 'status', 'filled_quantity', 'average_fill_price',
            'total_fees', 'created_at', 'updated_at', 'filled_at', 'cancelled_at',
            'notes', 'tags', 'remaining_quantity', 'fill_percentage', 'can_cancel'
        ]
        read_only_fields = [
            'id', 'user', 'filled_quantity', 'average_fill_price', 'total_fees',
            'created_at', 'updated_at', 'filled_at', 'cancelled_at'
        ]
    
    def get_remaining_quantity(self, obj):
        return obj.calculate_remaining_quantity()
    
    def get_fill_percentage(self, obj):
        return obj.calculate_fill_percentage()
    
    def get_can_cancel(self, obj):
        return obj.can_cancel()
    
    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be positive")
        return value
    
    def validate_price(self, value):
        """Validate price is positive if provided"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value
    
    def validate_stop_price(self, value):
        """Validate stop price is positive if provided"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Stop price must be positive")
        return value

class StopLossOrderSerializer(serializers.Serializer):
    """Serializer for stop-loss order creation"""
    symbol = serializers.CharField(max_length=20)
    side = serializers.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')])
    quantity = serializers.DecimalField(max_digits=20, decimal_places=8)
    stop_price = serializers.DecimalField(max_digits=20, decimal_places=8)
    time_in_force = serializers.CharField(max_length=10, default='GTC')
    expire_time = serializers.DateTimeField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )

class TakeProfitOrderSerializer(serializers.Serializer):
    """Serializer for take-profit order creation"""
    symbol = serializers.CharField(max_length=20)
    side = serializers.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')])
    quantity = serializers.DecimalField(max_digits=20, decimal_places=8)
    price = serializers.DecimalField(max_digits=20, decimal_places=8)
    time_in_force = serializers.CharField(max_length=10, default='GTC')
    expire_time = serializers.DateTimeField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )

class LimitOrderSerializer(serializers.Serializer):
    """Serializer for limit order creation"""
    symbol = serializers.CharField(max_length=20)
    side = serializers.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')])
    quantity = serializers.DecimalField(max_digits=20, decimal_places=8)
    price = serializers.DecimalField(max_digits=20, decimal_places=8)
    time_in_force = serializers.CharField(max_length=10, default='GTC')
    expire_time = serializers.DateTimeField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )

class MarketOrderSerializer(serializers.Serializer):
    """Serializer for market order creation"""
    symbol = serializers.CharField(max_length=20)
    side = serializers.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')])
    quantity = serializers.DecimalField(max_digits=20, decimal_places=8)
    notes = serializers.CharField(required=False, allow_blank=True)
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )

class StopLimitOrderSerializer(serializers.Serializer):
    """Serializer for stop-limit order creation"""
    symbol = serializers.CharField(max_length=20)
    side = serializers.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')])
    quantity = serializers.DecimalField(max_digits=20, decimal_places=8)
    stop_price = serializers.DecimalField(max_digits=20, decimal_places=8)
    limit_price = serializers.DecimalField(max_digits=20, decimal_places=8)
    time_in_force = serializers.CharField(max_length=10, default='GTC')
    expire_time = serializers.DateTimeField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )

class TradingStrategySerializer(serializers.ModelSerializer):
    """Serializer for TradingStrategy model"""
    win_rate = serializers.SerializerMethodField()
    avg_pnl = serializers.SerializerMethodField()
    
    class Meta:
        model = TradingStrategy
        fields = [
            'id', 'name', 'description', 'strategy_type', 'symbol', 'is_active',
            'parameters', 'max_position_size', 'stop_loss_percentage',
            'take_profit_percentage', 'total_trades', 'winning_trades',
            'losing_trades', 'total_pnl', 'created_at', 'updated_at',
            'last_executed', 'win_rate', 'avg_pnl'
        ]
        read_only_fields = [
            'id', 'user', 'total_trades', 'winning_trades', 'losing_trades',
            'total_pnl', 'created_at', 'updated_at', 'last_executed'
        ]
    
    def get_win_rate(self, obj):
        return obj.calculate_win_rate()
    
    def get_avg_pnl(self, obj):
        return obj.calculate_avg_pnl()
    
    def validate_max_position_size(self, value):
        """Validate max position size is positive if provided"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Max position size must be positive")
        return value
    
    def validate_stop_loss_percentage(self, value):
        """Validate stop loss percentage is between 0 and 100"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Stop loss percentage must be between 0 and 100")
        return value
    
    def validate_take_profit_percentage(self, value):
        """Validate take profit percentage is positive"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Take profit percentage must be positive")
        return value

class OrderExecutionSerializer(serializers.ModelSerializer):
    """Serializer for OrderExecution model"""
    class Meta:
        model = OrderExecution
        fields = [
            'id', 'execution_time', 'executed_quantity', 'execution_price',
            'fees', 'exchange_order_id'
        ]
        read_only_fields = ['id']

class StrategyExecutionSerializer(serializers.ModelSerializer):
    """Serializer for StrategyExecution model"""
    class Meta:
        model = StrategyExecution
        fields = [
            'id', 'execution_time', 'action', 'symbol', 'quantity', 'price',
            'reason', 'pnl'
        ]
        read_only_fields = ['id']

class OrderSummarySerializer(serializers.Serializer):
    """Serializer for order summary"""
    total_orders = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
    filled_orders = serializers.IntegerField()
    cancelled_orders = serializers.IntegerField()
    total_volume = serializers.DecimalField(max_digits=20, decimal_places=8)
    total_fees = serializers.DecimalField(max_digits=20, decimal_places=8)

class OrderHistorySerializer(serializers.Serializer):
    """Serializer for order history with pagination"""
    orders = AdvancedOrderSerializer(many=True)
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    total_count = serializers.IntegerField()
    has_next = serializers.BooleanField()
    has_previous = serializers.BooleanField()
