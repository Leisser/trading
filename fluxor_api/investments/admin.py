from django.contrib import admin
from .models import Investment, InvestmentTransaction


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'investment_type', 'status', 'total_invested_usd', 'current_value_usd', 'unrealized_pnl_percent', 'started_at']
    list_filter = ['investment_type', 'status', 'auto_compound', 'dca_frequency']
    search_fields = ['user__email', 'name']
    readonly_fields = ['started_at', 'last_updated']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'investment_type', 'status')
        }),
        ('Investment Target', {
            'fields': ('crypto_index', 'cryptocurrency')
        }),
        ('Investment Details', {
            'fields': ('total_invested_btc', 'total_invested_usd', 'current_value_btc', 'current_value_usd')
        }),
        ('Performance', {
            'fields': ('unrealized_pnl_btc', 'unrealized_pnl_usd', 'unrealized_pnl_percent', 'all_time_high_value', 'max_drawdown_percent')
        }),
        ('Strategy Settings', {
            'fields': ('auto_compound', 'dca_amount_btc', 'dca_frequency', 'next_dca_date')
        }),
        ('Timestamps', {
            'fields': ('started_at', 'closed_at', 'last_updated'),
            'classes': ('collapse',)
        })
    )


@admin.register(InvestmentTransaction)
class InvestmentTransactionAdmin(admin.ModelAdmin):
    list_display = ['investment', 'transaction_type', 'amount_btc', 'amount_usd', 'is_automatic', 'transaction_date']
    list_filter = ['transaction_type', 'is_automatic', 'transaction_date']
    search_fields = ['investment__name', 'investment__user__email']
    readonly_fields = ['transaction_date']
