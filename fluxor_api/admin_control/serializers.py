"""
Admin Control Serializers
"""
from rest_framework import serializers
from .models import TradingSettings, ProfitLossScenario, ScenarioExecution
from trades.models import CryptoIndex, Cryptocurrency


class TradingSettingsSerializer(serializers.ModelSerializer):
    """Serializer for TradingSettings model"""
    
    class Meta:
        model = TradingSettings
        fields = [
            'id', 'trading_enabled', 'maintenance_mode', 'profit_loss_mode',
            'default_profit_rate', 'default_loss_rate', 'max_profit_rate', 'max_loss_rate',
            'index_appreciation_rate', 'index_depreciation_rate', 'index_volatility_factor',
            'price_update_frequency', 'investment_update_frequency', 'portfolio_calculation_frequency',
            'min_trade_amount', 'max_trade_amount', 'min_investment_amount',
            'trading_fee_percentage', 'withdrawal_fee_percentage', 'management_fee_percentage',
            'created_at', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProfitLossScenarioSerializer(serializers.ModelSerializer):
    """Serializer for ProfitLossScenario model"""
    
    duration_in_seconds = serializers.ReadOnlyField()
    
    class Meta:
        model = ProfitLossScenario
        fields = [
            'id', 'name', 'description', 'scenario_type', 'percentage_change',
            'time_duration', 'time_unit', 'duration_in_seconds',
            'target_crypto_index', 'target_cryptocurrency', 'apply_to_all_investments',
            'apply_to_all_users', 'is_active', 'execute_immediately',
            'scheduled_execution', 'repeat_execution', 'repeat_interval_hours',
            'times_executed', 'last_executed', 'next_execution',
            'created_at', 'created_by', 'updated_at'
        ]
        read_only_fields = ['id', 'times_executed', 'last_executed', 'created_at', 'updated_at']


class CreateProfitLossScenarioSerializer(serializers.ModelSerializer):
    """Serializer for creating profit/loss scenarios"""
    
    class Meta:
        model = ProfitLossScenario
        fields = [
            'name', 'description', 'scenario_type', 'percentage_change',
            'time_duration', 'time_unit', 'target_crypto_index', 'target_cryptocurrency',
            'apply_to_all_investments', 'apply_to_all_users', 'execute_immediately',
            'scheduled_execution', 'repeat_execution', 'repeat_interval_hours'
        ]
    
    def validate(self, data):
        """Validate scenario data"""
        if not data.get('target_crypto_index') and not data.get('target_cryptocurrency') and not data.get('apply_to_all_investments'):
            raise serializers.ValidationError("Must specify a target (index, crypto, or all investments)")
        
        if data.get('target_crypto_index') and data.get('target_cryptocurrency'):
            raise serializers.ValidationError("Cannot specify both target_crypto_index and target_cryptocurrency")
        
        if data.get('percentage_change') == 0:
            raise serializers.ValidationError("Percentage change cannot be zero")
        
        return data


class ScenarioExecutionSerializer(serializers.ModelSerializer):
    """Serializer for ScenarioExecution model"""
    
    class Meta:
        model = ScenarioExecution
        fields = [
            'id', 'scenario', 'executed_at', 'executed_by', 'affected_investments',
            'affected_users', 'total_value_change', 'status', 'error_message'
        ]
        read_only_fields = ['id', 'executed_at']


class ExecuteScenarioSerializer(serializers.Serializer):
    """Serializer for executing scenarios"""
    
    force_execute = serializers.BooleanField(default=False)
    dry_run = serializers.BooleanField(default=False)
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)


class TradingSettingsUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating trading settings"""
    
    class Meta:
        model = TradingSettings
        fields = [
            'trading_enabled', 'maintenance_mode', 'profit_loss_mode',
            'default_profit_rate', 'default_loss_rate', 'max_profit_rate', 'max_loss_rate',
            'index_appreciation_rate', 'index_depreciation_rate', 'index_volatility_factor',
            'price_update_frequency', 'investment_update_frequency', 'portfolio_calculation_frequency',
            'min_trade_amount', 'max_trade_amount', 'min_investment_amount',
            'trading_fee_percentage', 'withdrawal_fee_percentage', 'management_fee_percentage'
        ]
    
    def validate(self, data):
        """Validate trading settings"""
        if data.get('default_profit_rate', 0) > data.get('max_profit_rate', 100):
            raise serializers.ValidationError("Default profit rate cannot exceed max profit rate")
        
        if data.get('default_loss_rate', 0) > data.get('max_loss_rate', 50):
            raise serializers.ValidationError("Default loss rate cannot exceed max loss rate")
        
        if data.get('min_trade_amount', 0) > data.get('max_trade_amount', 100):
            raise serializers.ValidationError("Min trade amount cannot exceed max trade amount")
        
        return data
