from rest_framework import serializers
from .models import TradingSettings, UserTradeOutcome, MarketDataSimulation


class TradingSettingsSerializer(serializers.ModelSerializer):
    """Serializer for admin trading settings"""
    
    class Meta:
        model = TradingSettings
        fields = [
            'id', 'is_active',
            # Idle Mode
            'idle_profit_percentage', 'idle_duration_seconds',
            # Active Mode
            'active_win_rate_percentage', 'active_profit_percentage',
            'active_loss_percentage', 'active_duration_seconds',
            # Legacy
            'win_rate_percentage', 'loss_rate_percentage',
            'min_profit_percentage', 'max_profit_percentage',
            'min_loss_percentage', 'max_loss_percentage',
            'min_trade_duration_seconds', 'max_trade_duration_seconds',
            'price_volatility_percentage', 'update_interval_seconds',
            # Real Prices
            'use_real_prices',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate settings"""
        # Validate win_rate for legacy compatibility
        win_rate = data.get('win_rate_percentage', 0)
        loss_rate = data.get('loss_rate_percentage', 0)
        
        if win_rate + loss_rate != 100:
            # Auto-adjust loss rate
            data['loss_rate_percentage'] = 100 - win_rate
        
        # Validate active_win_rate_percentage is 0-100
        active_win_rate = data.get('active_win_rate_percentage')
        if active_win_rate is not None:
            if active_win_rate < 0 or active_win_rate > 100:
                raise serializers.ValidationError({
                    'active_win_rate_percentage': 'Must be between 0 and 100'
                })
        
        return data


class UserTradeOutcomeSerializer(serializers.ModelSerializer):
    """Serializer for user trade outcomes"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    cryptocurrency_symbol = serializers.CharField(source='trade.cryptocurrency.symbol', read_only=True)
    seconds_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = UserTradeOutcome
        fields = [
            'id', 'user_email', 'cryptocurrency_symbol', 'outcome',
            'outcome_percentage', 'duration_seconds', 'target_close_time',
            'seconds_remaining', 'is_executed', 'executed_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'executed_at']
    
    def get_seconds_remaining(self, obj):
        """Calculate seconds remaining until target close time"""
        from django.utils import timezone
        if obj.is_executed:
            return 0
        remaining = (obj.target_close_time - timezone.now()).total_seconds()
        return max(0, int(remaining))


class MarketDataSimulationSerializer(serializers.ModelSerializer):
    """Serializer for market data simulation"""
    
    class Meta:
        model = MarketDataSimulation
        fields = [
            'id', 'cryptocurrency_symbol', 'timestamp',
            'open_price', 'high_price', 'low_price', 'close_price', 'volume'
        ]
        read_only_fields = ['id', 'timestamp']
