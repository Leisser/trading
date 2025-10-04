from django.contrib import admin
from .models import Portfolio, Position, PortfolioBalance, PortfolioSnapshot, PortfolioPerformance, AssetAllocation

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'portfolio_type', 'is_active', 'is_default', 'created_at')
    list_filter = ('portfolio_type', 'is_active', 'is_default', 'created_at')
    search_fields = ('name', 'user__email', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'portfolio_type', 'description')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_default')
        }),
        ('Risk Management', {
            'fields': ('max_position_size', 'max_leverage', 'stop_loss_percentage'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('trading_pair', 'portfolio', 'side', 'quantity', 'average_entry_price', 'current_price', 'unrealized_pnl', 'is_open')
    list_filter = ('side', 'is_open', 'is_hedged', 'opened_at', 'portfolio__portfolio_type')
    search_fields = ('trading_pair', 'portfolio__name', 'portfolio__user__email')
    readonly_fields = ('opened_at', 'closed_at', 'updated_at')
    ordering = ('-opened_at',)
    
    fieldsets = (
        ('Position Details', {
            'fields': ('portfolio', 'trading_pair', 'base_currency', 'quote_currency', 'side')
        }),
        ('Quantities and Prices', {
            'fields': ('quantity', 'average_entry_price', 'current_price', 'leverage')
        }),
        ('P&L Information', {
            'fields': ('unrealized_pnl', 'realized_pnl', 'total_pnl', 'position_value', 'margin_used')
        }),
        ('Risk Management', {
            'fields': ('stop_loss_price', 'take_profit_price'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_open', 'is_hedged')
        }),
        ('Timestamps', {
            'fields': ('opened_at', 'closed_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PortfolioBalance)
class PortfolioBalanceAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'currency', 'available_balance', 'locked_balance', 'total_balance', 'usd_value')
    list_filter = ('currency', 'updated_at')
    search_fields = ('portfolio__name', 'portfolio__user__email', 'currency')
    readonly_fields = ('updated_at',)
    ordering = ('portfolio__name', 'currency')

@admin.register(PortfolioSnapshot)
class PortfolioSnapshotAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'timestamp', 'total_value', 'total_pnl', 'daily_pnl', 'open_positions')
    list_filter = ('timestamp', 'portfolio__portfolio_type')
    search_fields = ('portfolio__name', 'portfolio__user__email')
    readonly_fields = ('created_at',)
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

@admin.register(PortfolioPerformance)
class PortfolioPerformanceAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'period', 'start_date', 'end_date', 'total_return', 'absolute_return', 'win_rate')
    list_filter = ('period', 'start_date', 'end_date')
    search_fields = ('portfolio__name', 'portfolio__user__email')
    readonly_fields = ('calculated_at',)
    ordering = ('-end_date',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('portfolio', 'period', 'start_date', 'end_date')
        }),
        ('Performance Metrics', {
            'fields': ('total_return', 'absolute_return', 'sharpe_ratio', 'sortino_ratio')
        }),
        ('Risk Metrics', {
            'fields': ('max_drawdown', 'volatility', 'beta', 'alpha'),
            'classes': ('collapse',)
        }),
        ('Trading Metrics', {
            'fields': ('total_trades', 'winning_trades', 'losing_trades', 'win_rate', 'average_trade'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('calculated_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(AssetAllocation)
class AssetAllocationAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'currency', 'allocation_percentage', 'allocation_value', 'currency_return', 'date')
    list_filter = ('currency', 'date')
    search_fields = ('portfolio__name', 'portfolio__user__email', 'currency')
    readonly_fields = ('created_at',)
    ordering = ('-date', 'allocation_percentage')
    date_hierarchy = 'date'
