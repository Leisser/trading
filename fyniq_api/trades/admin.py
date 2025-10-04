from django.contrib import admin
from .models import Trade

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'trade_type', 'btc_amount', 'usd_price', 'timestamp', 'status')
    list_filter = ('trade_type', 'status', 'timestamp')
    search_fields = ('user__email', 'notes')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',) 