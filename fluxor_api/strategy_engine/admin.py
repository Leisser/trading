from django.contrib import admin
from .models import TradingStrategy, StrategyExecution, StrategyPerformance, StrategyAlert


@admin.register(TradingStrategy)
class TradingStrategyAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'strategy_type', 'symbol', 'is_active', 'status', 'total_pnl', 'win_rate', 'created_at']
    list_filter = ['strategy_type', 'is_active', 'status', 'created_at']
    search_fields = ['user__email', 'name', 'symbol']
    readonly_fields = ['total_trades', 'winning_trades', 'losing_trades', 'total_pnl', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'description', 'strategy_type', 'symbol')
        }),
        ('Status', {
            'fields': ('is_active', 'status')
        }),
        ('Parameters', {
            'fields': ('parameters', 'max_position_size', 'stop_loss_percentage', 'take_profit_percentage')
        }),
        ('Performance', {
            'fields': ('total_trades', 'winning_trades', 'losing_trades', 'total_pnl')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_executed', 'started_at', 'stopped_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(StrategyExecution)
class StrategyExecutionAdmin(admin.ModelAdmin):
    list_display = ['strategy', 'execution_time', 'action', 'symbol', 'quantity', 'price', 'pnl']
    list_filter = ['action', 'execution_time', 'strategy__strategy_type']
    search_fields = ['strategy__name', 'strategy__user__email', 'symbol']
    readonly_fields = ['execution_time']


@admin.register(StrategyPerformance)
class StrategyPerformanceAdmin(admin.ModelAdmin):
    list_display = ['strategy', 'date', 'daily_pnl', 'daily_trades', 'cumulative_pnl', 'max_drawdown']
    list_filter = ['date', 'strategy__strategy_type']
    search_fields = ['strategy__name', 'strategy__user__email']
    readonly_fields = ['created_at']


@admin.register(StrategyAlert)
class StrategyAlertAdmin(admin.ModelAdmin):
    list_display = ['strategy', 'alert_type', 'title', 'is_read', 'is_urgent', 'created_at']
    list_filter = ['alert_type', 'is_read', 'is_urgent', 'created_at']
    search_fields = ['strategy__name', 'strategy__user__email', 'title', 'message']
    readonly_fields = ['created_at']
