"""
Serializers for Market Data API.
"""
from rest_framework import serializers
from decimal import Decimal
from .models import Exchange, TradingPair, MarketData, PriceAlert

class ExchangeSerializer(serializers.ModelSerializer):
    """Serializer for Exchange model"""
    class Meta:
        model = Exchange
        fields = ['id', 'name', 'code', 'api_url', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TradingPairSerializer(serializers.ModelSerializer):
    """Serializer for TradingPair model"""
    exchange_name = serializers.CharField(source='exchange.name', read_only=True)
    
    class Meta:
        model = TradingPair
        fields = [
            'id', 'exchange', 'exchange_name', 'base_currency', 'quote_currency', 
            'symbol', 'is_active', 'min_order_size', 'max_order_size', 
            'price_precision', 'quantity_precision', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class MarketDataSerializer(serializers.ModelSerializer):
    """Serializer for MarketData model"""
    symbol = serializers.CharField(source='trading_pair.symbol', read_only=True)
    exchange = serializers.CharField(source='trading_pair.exchange.name', read_only=True)
    
    class Meta:
        model = MarketData
        fields = [
            'id', 'trading_pair', 'symbol', 'exchange', 'timestamp', 
            'open_price', 'high_price', 'low_price', 'close_price', 
            'volume', 'quote_volume'
        ]
        read_only_fields = ['id']

class PriceAlertSerializer(serializers.ModelSerializer):
    """Serializer for PriceAlert model"""
    class Meta:
        model = PriceAlert
        fields = [
            'id', 'user', 'symbol', 'target_price', 'condition', 
            'message', 'is_active', 'is_triggered', 'triggered_at', 
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'is_triggered', 'triggered_at', 'created_at']
    
    def validate_target_price(self, value):
        """Validate target price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Target price must be positive")
        return value
    
    def validate_condition(self, value):
        """Validate condition is valid"""
        if value not in ['above', 'below']:
            raise serializers.ValidationError("Condition must be 'above' or 'below'")
        return value

class TechnicalAnalysisSerializer(serializers.Serializer):
    """Serializer for technical analysis data"""
    symbol = serializers.CharField()
    timeframe = serializers.CharField()
    period = serializers.IntegerField()
    indicators = serializers.DictField()
    current_price = serializers.DecimalField(max_digits=20, decimal_places=8, allow_null=True)
    timestamp = serializers.DateTimeField()

class RealTimePriceSerializer(serializers.Serializer):
    """Serializer for real-time price data"""
    symbol = serializers.CharField()
    exchange = serializers.CharField()
    price = serializers.DecimalField(max_digits=20, decimal_places=8)
    bid = serializers.DecimalField(max_digits=20, decimal_places=8)
    ask = serializers.DecimalField(max_digits=20, decimal_places=8)
    volume = serializers.DecimalField(max_digits=20, decimal_places=8)
    change_24h = serializers.DecimalField(max_digits=20, decimal_places=8)
    change_percent_24h = serializers.DecimalField(max_digits=5, decimal_places=2)
    high_24h = serializers.DecimalField(max_digits=20, decimal_places=8)
    low_24h = serializers.DecimalField(max_digits=20, decimal_places=8)
    timestamp = serializers.DateTimeField()

class OHLCVSerializer(serializers.Serializer):
    """Serializer for OHLCV data"""
    timestamp = serializers.DateTimeField()
    open = serializers.DecimalField(max_digits=20, decimal_places=8)
    high = serializers.DecimalField(max_digits=20, decimal_places=8)
    low = serializers.DecimalField(max_digits=20, decimal_places=8)
    close = serializers.DecimalField(max_digits=20, decimal_places=8)
    volume = serializers.DecimalField(max_digits=20, decimal_places=8)

class OrderBookSerializer(serializers.Serializer):
    """Serializer for order book data"""
    symbol = serializers.CharField()
    exchange = serializers.CharField()
    bids = serializers.ListField(
        child=serializers.ListField(
            child=serializers.DecimalField(max_digits=20, decimal_places=8),
            min_length=2,
            max_length=2
        )
    )
    asks = serializers.ListField(
        child=serializers.ListField(
            child=serializers.DecimalField(max_digits=20, decimal_places=8),
            min_length=2,
            max_length=2
        )
    )
    timestamp = serializers.DateTimeField()

class TradingPairListSerializer(serializers.Serializer):
    """Serializer for trading pair list"""
    symbol = serializers.CharField()
    base = serializers.CharField()
    quote = serializers.CharField()
    active = serializers.BooleanField()
    precision = serializers.DictField()
    limits = serializers.DictField()
