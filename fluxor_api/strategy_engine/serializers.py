"""
Strategy Engine Serializers
"""
from rest_framework import serializers
from .models import TradingStrategy, StrategyExecution, StrategyPerformance, StrategyAlert


class TradingStrategySerializer(serializers.ModelSerializer):
    """Serializer for TradingStrategy model"""
    
    win_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = TradingStrategy
        fields = [
            'id', 'user', 'name', 'description', 'strategy_type', 'symbol',
            'is_active', 'status', 'parameters', 'max_position_size',
            'stop_loss_percentage', 'take_profit_percentage', 'total_trades',
            'winning_trades', 'losing_trades', 'total_pnl', 'win_rate',
            'created_at', 'updated_at', 'last_executed', 'started_at', 'stopped_at'
        ]
        read_only_fields = ['id', 'user', 'total_trades', 'winning_trades', 'losing_trades', 'total_pnl', 'created_at', 'updated_at']


class CreateTradingStrategySerializer(serializers.ModelSerializer):
    """Serializer for creating trading strategies"""
    
    class Meta:
        model = TradingStrategy
        fields = [
            'name', 'description', 'strategy_type', 'symbol', 'parameters',
            'max_position_size', 'stop_loss_percentage', 'take_profit_percentage'
        ]
    
    def validate(self, data):
        """Validate strategy data"""
        strategy_type = data.get('strategy_type')
        parameters = data.get('parameters', {})
        
        # Validate strategy-specific parameters
        if strategy_type == 'dca':
            if 'amount' not in parameters or 'frequency' not in parameters:
                raise serializers.ValidationError("DCA strategy requires 'amount' and 'frequency' parameters")
        
        elif strategy_type == 'grid':
            if 'grid_size' not in parameters or 'grid_count' not in parameters:
                raise serializers.ValidationError("Grid strategy requires 'grid_size' and 'grid_count' parameters")
        
        elif strategy_type == 'momentum':
            if 'lookback_period' not in parameters or 'threshold' not in parameters:
                raise serializers.ValidationError("Momentum strategy requires 'lookback_period' and 'threshold' parameters")
        
        return data


class StrategyExecutionSerializer(serializers.ModelSerializer):
    """Serializer for StrategyExecution model"""
    
    class Meta:
        model = StrategyExecution
        fields = [
            'id', 'strategy', 'execution_time', 'action', 'symbol', 'quantity',
            'price', 'reason', 'pnl', 'market_conditions', 'strategy_parameters'
        ]
        read_only_fields = ['id', 'execution_time']


class StrategyPerformanceSerializer(serializers.ModelSerializer):
    """Serializer for StrategyPerformance model"""
    
    class Meta:
        model = StrategyPerformance
        fields = [
            'id', 'strategy', 'date', 'daily_pnl', 'daily_trades', 'daily_win_rate',
            'cumulative_pnl', 'cumulative_trades', 'cumulative_win_rate',
            'max_drawdown', 'sharpe_ratio', 'volatility', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class StrategyAlertSerializer(serializers.ModelSerializer):
    """Serializer for StrategyAlert model"""
    
    class Meta:
        model = StrategyAlert
        fields = [
            'id', 'strategy', 'alert_type', 'title', 'message', 'is_read',
            'is_urgent', 'alert_data', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ExecuteStrategySerializer(serializers.Serializer):
    """Serializer for executing strategies"""
    
    dry_run = serializers.BooleanField(default=False)
    force_execute = serializers.BooleanField(default=False)
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)


class StrategyAnalyticsSerializer(serializers.Serializer):
    """Serializer for strategy analytics data"""
    
    strategy_id = serializers.IntegerField()
    strategy_name = serializers.CharField()
    strategy_type = serializers.CharField()
    total_pnl = serializers.DecimalField(max_digits=20, decimal_places=8)
    total_trades = serializers.IntegerField()
    win_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    max_drawdown = serializers.DecimalField(max_digits=10, decimal_places=4)
    sharpe_ratio = serializers.DecimalField(max_digits=10, decimal_places=4)
    is_active = serializers.BooleanField()
    last_executed = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class StrategyBacktestSerializer(serializers.Serializer):
    """Serializer for strategy backtesting"""
    
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    initial_capital = serializers.DecimalField(max_digits=20, decimal_places=8)
    parameters = serializers.JSONField()
    
    def validate(self, data):
        """Validate backtest data"""
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Start date must be before end date")
        
        if data['initial_capital'] <= 0:
            raise serializers.ValidationError("Initial capital must be greater than 0")
        
        return data
