from django.contrib import admin
from .models import Exchange, TradingPair, MarketData, Ticker, OrderBook, Trade, MarketDataAggregation

@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'api_url', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)

@admin.register(TradingPair)
class TradingPairAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'exchange', 'base_currency', 'quote_currency', 'is_active', 'created_at')
    list_filter = ('exchange', 'is_active', 'created_at')
    search_fields = ('symbol', 'base_currency', 'quote_currency')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('symbol',)

@admin.register(MarketData)
class MarketDataAdmin(admin.ModelAdmin):
    list_display = ('trading_pair', 'timestamp', 'open_price', 'high_price', 'low_price', 'close_price', 'volume')
    list_filter = ('trading_pair__exchange', 'trading_pair__symbol', 'timestamp')
    search_fields = ('trading_pair__symbol',)
    readonly_fields = ('created_at',)
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ('trading_pair', 'timestamp', 'last_price', 'bid_price', 'ask_price', 'volume_24h')
    list_filter = ('trading_pair__exchange', 'trading_pair__symbol', 'timestamp')
    search_fields = ('trading_pair__symbol',)
    readonly_fields = ('created_at',)
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

@admin.register(OrderBook)
class OrderBookAdmin(admin.ModelAdmin):
    list_display = ('trading_pair', 'timestamp', 'side', 'price', 'quantity')
    list_filter = ('trading_pair__exchange', 'trading_pair__symbol', 'side', 'timestamp')
    search_fields = ('trading_pair__symbol',)
    readonly_fields = ('created_at',)
    ordering = ('-timestamp', 'side', 'price')

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('trading_pair', 'timestamp', 'side', 'price', 'quantity', 'quote_quantity')
    list_filter = ('trading_pair__exchange', 'trading_pair__symbol', 'side', 'timestamp')
    search_fields = ('trading_pair__symbol', 'exchange_trade_id')
    readonly_fields = ('created_at',)
    ordering = ('-timestamp',)

@admin.register(MarketDataAggregation)
class MarketDataAggregationAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'timestamp', 'weighted_average_price', 'total_volume', 'number_of_exchanges')
    list_filter = ('symbol', 'timestamp')
    search_fields = ('symbol',)
    readonly_fields = ('created_at',)
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
