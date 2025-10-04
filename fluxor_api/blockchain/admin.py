from django.contrib import admin
from .models import BlockchainMonitor, Transaction, Block, MempoolTransaction, NetworkStats

@admin.register(BlockchainMonitor)
class BlockchainMonitorAdmin(admin.ModelAdmin):
    list_display = ['status', 'message', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['message']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        return False  # Only allow viewing, not manual creation

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id', 'transaction_type', 'amount', 'fee', 
        'status', 'confirmations', 'timestamp', 'from_address', 'to_address'
    ]
    list_filter = [
        'transaction_type', 'status', 'confirmations', 'timestamp'
    ]
    search_fields = [
        'tx_hash', 'from_address', 'to_address', 'transaction_id'
    ]
    readonly_fields = [
        'transaction_id', 'timestamp', 'confirmed_at'
    ]
    fieldsets = (
        ('Basic Information', {
            'fields': ('transaction_id', 'tx_hash', 'block_height')
        }),
        ('Transaction Details', {
            'fields': ('transaction_type', 'amount', 'fee')
        }),
        ('Addresses', {
            'fields': ('from_address', 'to_address')
        }),
        ('Status', {
            'fields': ('status', 'confirmations', 'confirmed_at')
        }),
        ('Metadata', {
            'fields': ('notes', 'raw_data', 'timestamp')
        })
    )
    ordering = ['-timestamp']

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = [
        'block_height', 'block_hash', 'timestamp', 'difficulty', 
        'transaction_count', 'size', 'weight'
    ]
    list_filter = ['timestamp']
    search_fields = ['block_hash', 'block_height']
    readonly_fields = [
        'block_height', 'block_hash', 'timestamp', 'difficulty'
    ]
    fieldsets = (
        ('Block Information', {
            'fields': ('block_height', 'block_hash', 'previous_block_hash', 'merkle_root')
        }),
        ('Block Details', {
            'fields': ('timestamp', 'difficulty', 'nonce')
        }),
        ('Size and Transactions', {
            'fields': ('size', 'weight', 'transaction_count')
        }),
        ('Mining Info', {
            'fields': ('miner_address', 'block_reward')
        })
    )
    ordering = ['-block_height']

@admin.register(MempoolTransaction)
class MempoolTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'tx_hash', 'fee_rate', 'fee', 'size', 'weight', 
        'is_confirmed', 'first_seen'
    ]
    list_filter = ['is_confirmed', 'first_seen', 'last_updated']
    search_fields = ['tx_hash']
    readonly_fields = ['first_seen', 'last_updated']
    fieldsets = (
        ('Transaction Info', {
            'fields': ('tx_hash', 'fee_rate', 'fee')
        }),
        ('Size Information', {
            'fields': ('size', 'weight')
        }),
        ('Status', {
            'fields': ('is_confirmed', 'confirmed_in_block')
        }),
        ('Timestamps', {
            'fields': ('first_seen', 'last_updated')
        })
    )
    ordering = ['-fee_rate']

@admin.register(NetworkStats)
class NetworkStatsAdmin(admin.ModelAdmin):
    list_display = [
        'timestamp', 'current_difficulty', 'hash_rate', 'block_time',
        'mempool_size', 'btc_price_usd', 'market_cap'
    ]
    list_filter = ['timestamp']
    readonly_fields = ['timestamp']
    fieldsets = (
        ('Network Metrics', {
            'fields': ('current_difficulty', 'hash_rate', 'block_time')
        }),
        ('Mempool Metrics', {
            'fields': ('mempool_size', 'mempool_bytes', 'mempool_fee_rate')
        }),
        ('Market Data', {
            'fields': ('btc_price_usd', 'market_cap', 'volume_24h')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        })
    )
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        return False  # Only allow viewing, not manual creation 