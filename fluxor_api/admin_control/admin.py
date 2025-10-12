from django.contrib import admin
from .models import TradingSettings, UserTradeOutcome, MarketDataSimulation


@admin.register(TradingSettings)
class TradingSettingsAdmin(admin.ModelAdmin):
    list_display = ['is_active', 'active_win_rate_percentage', 'active_profit_percentage', 'active_loss_percentage', 'updated_at']
    list_filter = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Status', {
            'fields': ('is_active',)
        }),
        ('🟢 IDLE MODE (No Active Trading)', {
            'fields': ('idle_profit_percentage', 'idle_duration_seconds'),
            'description': 'Settings when no users have traded in the last 10 minutes'
        }),
        ('🔴 ACTIVE MODE (Users Trading)', {
            'fields': (
                'active_win_rate_percentage',
                'active_profit_percentage', 
                'active_loss_percentage',
                'active_duration_seconds'
            ),
            'description': 'Settings when users are actively trading'
        }),
        ('Legacy Win/Loss Configuration', {
            'fields': ('win_rate_percentage', 'loss_rate_percentage'),
            'classes': ('collapse',)
        }),
        ('Profit Magnitude', {
            'fields': ('min_profit_percentage', 'max_profit_percentage'),
            'classes': ('collapse',)
        }),
        ('Loss Magnitude', {
            'fields': ('min_loss_percentage', 'max_loss_percentage'),
            'classes': ('collapse',)
        }),
        ('Time Periods', {
            'fields': ('min_trade_duration_seconds', 'max_trade_duration_seconds'),
            'classes': ('collapse',)
        }),
        ('Market Simulation', {
            'fields': ('price_volatility_percentage', 'update_interval_seconds'),
            'classes': ('collapse',)
        }),
        ('🌐 Real Price Integration', {
            'fields': ('use_real_prices',),
            'description': 'Enable fetching real cryptocurrency prices from exchanges (CoinGecko/CCXT)'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'updated_by'),
            'classes': ('collapse',)
        })
    )


@admin.register(UserTradeOutcome)
class UserTradeOutcomeAdmin(admin.ModelAdmin):
    list_display = ['user', 'outcome', 'outcome_percentage', 'duration_seconds', 'is_executed', 'created_at']
    list_filter = ['outcome', 'is_executed']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'executed_at']


@admin.register(MarketDataSimulation)
class MarketDataSimulationAdmin(admin.ModelAdmin):
    list_display = ['cryptocurrency_symbol', 'close_price', 'volume', 'timestamp']
    list_filter = ['cryptocurrency_symbol']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
