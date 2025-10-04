from rest_framework import serializers
from decimal import Decimal
import random

class PriceFeedSerializer(serializers.Serializer):
    """
    Serializer for real-time price feed data.
    
    Example Response:
    {
        "symbol": "BTC/USDT",
        "binance_price": 45000.00,
        "coingecko_price": 44985.50,
        "price_change_24h": 2.5,
        "volume_24h": 2500000000,
        "high_24h": 45500.00,
        "low_24h": 44000.00,
        "timestamp": "2024-01-01T12:00:00Z"
    }
    """
    symbol = serializers.CharField(help_text="Trading pair symbol")
    binance_price = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Price from Binance")
    coingecko_price = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Price from CoinGecko")
    price_change_24h = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="24h price change percentage")
    volume_24h = serializers.DecimalField(max_digits=15, decimal_places=2, help_text="24h trading volume")
    high_24h = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="24h high price")
    low_24h = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="24h low price")
    timestamp = serializers.DateTimeField(help_text="Price timestamp")

class TradingSignalSerializer(serializers.Serializer):
    """
    Serializer for trading signals from algorithms.
    
    Example Response:
    {
        "signal": "buy",
        "confidence": 0.85,
        "indicators": {
            "rsi": 35.2,
            "sma": 44800.00,
            "ema": 44950.00,
            "macd": 150.00
        },
        "reasoning": "RSI indicates oversold conditions, MACD shows bullish momentum",
        "timestamp": "2024-01-01T12:00:00Z"
    }
    """
    signal = serializers.ChoiceField(
        choices=[('buy', 'Buy'), ('sell', 'Sell'), ('hold', 'Hold')],
        help_text="Trading signal recommendation"
    )
    confidence = serializers.DecimalField(
        max_digits=3, 
        decimal_places=2,
        min_value=0.0,
        max_value=1.0,
        help_text="Signal confidence level (0.0 to 1.0)"
    )
    indicators = serializers.DictField(help_text="Technical indicators values")
    reasoning = serializers.CharField(help_text="Explanation for the signal")
    timestamp = serializers.DateTimeField(help_text="Signal timestamp")

class AdvancedTradeExecutionSerializer(serializers.Serializer):
    """
    Serializer for advanced trade execution with risk management.
    
    Example Request:
    {
        "trade_type": "buy",
        "amount": 1000.00,
        "leverage": 2.0,
        "stop_loss": 44000.00,
        "take_profit": 46000.00
    }
    
    Example Response:
    {
        "status": "Trade executed (simulated)",
        "trade_id": "T123456789",
        "executed_price": 45000.00,
        "btc_amount": "0.04444444",
        "leverage_used": 2.0,
        "position_size": 2000.00,
        "risk_check": "passed",
        "compliance_check": "passed",
        "stop_loss": 44000.00,
        "take_profit": 46000.00,
        "timestamp": "2024-01-01T12:00:00Z"
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
    stop_loss = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text="Stop loss price (optional)"
    )
    take_profit = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text="Take profit price (optional)"
    )

class TradeExecutionResponseSerializer(serializers.Serializer):
    """
    Serializer for trade execution response.
    """
    status = serializers.CharField(help_text="Execution status")
    trade_id = serializers.CharField(help_text="Unique trade identifier")
    executed_price = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Price at execution")
    btc_amount = serializers.CharField(help_text="BTC amount traded")
    leverage_used = serializers.DecimalField(max_digits=3, decimal_places=1, help_text="Leverage used")
    position_size = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Total position size")
    risk_check = serializers.CharField(help_text="Risk management check result")
    compliance_check = serializers.CharField(help_text="Compliance check result")
    stop_loss = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, help_text="Stop loss price")
    take_profit = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, help_text="Take profit price")
    timestamp = serializers.DateTimeField(help_text="Execution timestamp")

class OHLCVSerializer(serializers.Serializer):
    """
    Serializer for OHLCV (Open, High, Low, Close, Volume) data.
    
    Example Response:
    {
        "symbol": "BTC/USDT",
        "timeframe": "1m",
        "data": [
            {
                "timestamp": "2024-01-01T12:00:00Z",
                "open": 45000.00,
                "high": 45100.00,
                "low": 44900.00,
                "close": 45050.00,
                "volume": 1250.50
            }
        ]
    }
    """
    symbol = serializers.CharField(help_text="Trading pair symbol")
    timeframe = serializers.CharField(help_text="Timeframe (1m, 5m, 15m, 1h, 4h, 1d)")
    data = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of OHLCV data points"
    )

class TechnicalIndicatorsSerializer(serializers.Serializer):
    """
    Serializer for technical indicators data.
    
    Example Response:
    {
        "symbol": "BTC/USDT",
        "timestamp": "2024-01-01T12:00:00Z",
        "indicators": {
            "rsi": 45.2,
            "sma_14": 44800.00,
            "sma_50": 44500.00,
            "ema_12": 44950.00,
            "ema_26": 44700.00,
            "macd": 250.00,
            "macd_signal": 200.00,
            "macd_histogram": 50.00,
            "bollinger_upper": 45500.00,
            "bollinger_middle": 45000.00,
            "bollinger_lower": 44500.00
        }
    }
    """
    symbol = serializers.CharField(help_text="Trading pair symbol")
    timestamp = serializers.DateTimeField(help_text="Data timestamp")
    indicators = serializers.DictField(help_text="Technical indicators values")

class MarketDataSerializer(serializers.Serializer):
    """
    Serializer for comprehensive market data.
    
    Example Response:
    {
        "symbol": "BTC/USDT",
        "current_price": 45000.00,
        "price_change_24h": 2.5,
        "price_change_percent_24h": 5.88,
        "market_cap": 850000000000,
        "volume_24h": 2500000000,
        "circulating_supply": 19500000,
        "max_supply": 21000000,
        "ath": 69000.00,
        "ath_change_percent": -34.78,
        "atl": 67.81,
        "atl_change_percent": 66250.00,
        "last_updated": "2024-01-01T12:00:00Z"
    }
    """
    symbol = serializers.CharField(help_text="Trading pair symbol")
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Current price")
    price_change_24h = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="24h price change")
    price_change_percent_24h = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="24h price change percentage")
    market_cap = serializers.DecimalField(max_digits=15, decimal_places=2, help_text="Market capitalization")
    volume_24h = serializers.DecimalField(max_digits=15, decimal_places=2, help_text="24h trading volume")
    circulating_supply = serializers.DecimalField(max_digits=15, decimal_places=2, help_text="Circulating supply")
    max_supply = serializers.DecimalField(max_digits=15, decimal_places=2, help_text="Maximum supply")
    ath = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="All-time high price")
    ath_change_percent = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="ATH change percentage")
    atl = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="All-time low price")
    atl_change_percent = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="ATL change percentage")
    last_updated = serializers.DateTimeField(help_text="Last update timestamp")

class WebSocketMessageSerializer(serializers.Serializer):
    """
    Serializer for WebSocket messages.
    
    Example:
    {
        "type": "price_update",
        "data": {
            "symbol": "BTC/USDT",
            "price": 45000.00,
            "timestamp": "2024-01-01T12:00:00Z"
        }
    }
    """
    type = serializers.CharField(help_text="Message type")
    data = serializers.DictField(help_text="Message data")

class ExecuteTradeSerializer(serializers.Serializer):
    """
    Serializer for trade execution requests.
    
    Example Request:
    {
        "side": "buy",
        "amount": "0.001",
        "price": "45000.00",
        "symbol": "BTC/USD",
        "leverage": 1.0,
        "stop_loss": "44000.00",
        "take_profit": "46000.00"
    }
    """
    side = serializers.ChoiceField(
        choices=[('buy', 'Buy'), ('sell', 'Sell')],
        help_text="Trade side (buy or sell)"
    )
    amount = serializers.CharField(help_text="Amount to trade")
    price = serializers.CharField(required=False, help_text="Limit price (optional for market orders)")
    symbol = serializers.CharField(default='BTC/USD', help_text="Trading pair symbol")
    leverage = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=1.0,
        min_value=1.0,
        max_value=10.0,
        help_text="Leverage multiplier"
    )
    stop_loss = serializers.CharField(required=False, help_text="Stop loss price")
    take_profit = serializers.CharField(required=False, help_text="Take profit price")
    
    def validate_amount(self, value):
        """Convert amount to Decimal for proper comparison"""
        try:
            amount = Decimal(str(value))
            if amount <= 0:
                raise serializers.ValidationError("Amount must be positive")
            return amount
        except (ValueError, TypeError):
            raise serializers.ValidationError("Invalid amount format")
    
    def validate_price(self, value):
        """Convert price to Decimal if provided"""
        if value is not None:
            try:
                return Decimal(str(value))
            except (ValueError, TypeError):
                raise serializers.ValidationError("Invalid price format")
        return value

class TradingStrategySerializer(serializers.Serializer):
    """
    Serializer for trading strategy configuration.
    
    Example Request:
    {
        "name": "RSI Strategy",
        "symbol": "BTC/USD",
        "parameters": {
            "rsi_period": 14,
            "rsi_oversold": 30,
            "rsi_overbought": 70
        }
    }
    """
    name = serializers.CharField(help_text="Strategy name")
    symbol = serializers.CharField(help_text="Trading pair symbol")
    parameters = serializers.DictField(help_text="Strategy parameters")
    
    def validate_parameters(self, value):
        """Validate strategy parameters."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Parameters must be a dictionary")
        return value

class OrderBookSerializer(serializers.Serializer):
    """
    Serializer for order book data.
    
    Example Response:
    {
        "symbol": "BTC/USD",
        "timestamp": "2024-01-01T12:00:00Z",
        "bids": [["45000.00", "0.5"], ["44999.00", "1.2"]],
        "asks": [["45001.00", "0.3"], ["45002.00", "0.7"]],
        "spread": "1.00",
        "spread_percent": "0.002"
    }
    """
    symbol = serializers.CharField(help_text="Trading pair symbol")
    timestamp = serializers.DateTimeField(help_text="Order book timestamp")
    bids = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField()),
        help_text="Bid orders [price, amount]"
    )
    asks = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField()),
        help_text="Ask orders [price, amount]"
    )
    spread = serializers.CharField(help_text="Bid-ask spread")
    spread_percent = serializers.CharField(help_text="Spread as percentage") 