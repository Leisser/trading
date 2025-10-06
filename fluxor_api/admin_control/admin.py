from django.contrib import admin
from .models import TradingSettings, ProfitLossScenario, ScenarioExecution


@admin.register(TradingSettings)
class TradingSettingsAdmin(admin.ModelAdmin):
    list_display = ['trading_enabled', 'maintenance_mode', 'profit_loss_mode', 'default_profit_rate', 'default_loss_rate', 'updated_at']
    list_filter = ['trading_enabled', 'maintenance_mode', 'profit_loss_mode']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Global Settings', {
            'fields': ('trading_enabled', 'maintenance_mode', 'profit_loss_mode')
        }),
        ('Profit/Loss Rates', {
            'fields': ('default_profit_rate', 'default_loss_rate', 'max_profit_rate', 'max_loss_rate')
        }),
        ('Index Settings', {
            'fields': ('index_appreciation_rate', 'index_depreciation_rate', 'index_volatility_factor')
        }),
        ('Update Frequencies', {
            'fields': ('price_update_frequency', 'investment_update_frequency', 'portfolio_calculation_frequency')
        }),
        ('Trading Limits', {
            'fields': ('min_trade_amount', 'max_trade_amount', 'min_investment_amount')
        }),
        ('Fees', {
            'fields': ('trading_fee_percentage', 'withdrawal_fee_percentage', 'management_fee_percentage')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'updated_by'),
            'classes': ('collapse',)
        })
    )


@admin.register(ProfitLossScenario)
class ProfitLossScenarioAdmin(admin.ModelAdmin):
    list_display = ['name', 'scenario_type', 'percentage_change', 'time_duration', 'time_unit', 'is_active', 'times_executed', 'created_at']
    list_filter = ['scenario_type', 'is_active', 'apply_to_all_investments', 'apply_to_all_users', 'repeat_execution']
    search_fields = ['name', 'description']
    readonly_fields = ['times_executed', 'last_executed', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'scenario_type')
        }),
        ('Parameters', {
            'fields': ('percentage_change', 'time_duration', 'time_unit')
        }),
        ('Target Settings', {
            'fields': ('target_crypto_index', 'target_cryptocurrency', 'apply_to_all_investments', 'apply_to_all_users')
        }),
        ('Execution Settings', {
            'fields': ('is_active', 'execute_immediately', 'scheduled_execution', 'repeat_execution', 'repeat_interval_hours')
        }),
        ('Tracking', {
            'fields': ('times_executed', 'last_executed', 'next_execution'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'created_by', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(ScenarioExecution)
class ScenarioExecutionAdmin(admin.ModelAdmin):
    list_display = ['scenario', 'executed_at', 'executed_by', 'affected_investments', 'affected_users', 'status']
    list_filter = ['status', 'executed_at', 'scenario__scenario_type']
    search_fields = ['scenario__name', 'executed_by__email']
    readonly_fields = ['executed_at']
    
    fieldsets = (
        ('Execution Details', {
            'fields': ('scenario', 'executed_at', 'executed_by')
        }),
        ('Results', {
            'fields': ('affected_investments', 'affected_users', 'total_value_change', 'status')
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        })
    )
