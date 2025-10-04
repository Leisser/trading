from django.contrib import admin
from .models import Order, OrderFill, OrderBook, OrderTemplate, OrderAlgo

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'trading_pair', 'side', 'order_type', 'quantity', 'price', 'status', 'created_at')
    list_filter = ('status', 'order_type', 'side', 'trading_pair', 'created_at')
    search_fields = ('order_id', 'user__email', 'trading_pair', 'client_order_id')
    readonly_fields = ('created_at', 'updated_at', 'filled_at', 'cancelled_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'order_id', 'exchange_order_id', 'client_order_id')
        }),
        ('Trading Details', {
            'fields': ('trading_pair', 'base_currency', 'quote_currency', 'side', 'order_type')
        }),
        ('Order Specifications', {
            'fields': ('quantity', 'price', 'stop_price', 'take_profit_price', 'time_in_force')
        }),
        ('Execution Status', {
            'fields': ('status', 'filled_quantity', 'average_fill_price', 'total_quote_amount')
        }),
        ('Fees', {
            'fields': ('fee', 'fee_currency')
        }),
        ('Advanced Options', {
            'fields': ('is_post_only', 'reduce_only', 'iceberg_quantity')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'filled_at', 'cancelled_at', 'expires_at'),
            'classes': ('collapse',)
        }),
        ('Additional', {
            'fields': ('notes', 'metadata'),
            'classes': ('collapse',)
        }),
    )

@admin.register(OrderFill)
class OrderFillAdmin(admin.ModelAdmin):
    list_display = ('fill_id', 'order', 'quantity', 'price', 'quote_amount', 'filled_at')
    list_filter = ('filled_at', 'fee_currency')
    search_fields = ('fill_id', 'order__order_id', 'exchange_fill_id')
    readonly_fields = ('created_at',)
    ordering = ('-filled_at',)
    date_hierarchy = 'filled_at'

@admin.register(OrderBook)
class OrderBookAdmin(admin.ModelAdmin):
    list_display = ('trading_pair', 'exchange', 'timestamp', 'sequence_number')
    list_filter = ('trading_pair', 'exchange', 'timestamp')
    search_fields = ('trading_pair', 'exchange')
    readonly_fields = ('created_at',)
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

@admin.register(OrderTemplate)
class OrderTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'template_type', 'trading_pair', 'order_type', 'side', 'is_active')
    list_filter = ('template_type', 'order_type', 'side', 'is_active', 'created_at')
    search_fields = ('name', 'user__email', 'trading_pair')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)

@admin.register(OrderAlgo)
class OrderAlgoAdmin(admin.ModelAdmin):
    list_display = ('order', 'algo_type', 'is_active', 'executed_chunks', 'total_chunks', 'start_time')
    list_filter = ('algo_type', 'is_active', 'start_time')
    search_fields = ('order__order_id', 'algo_type')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
