from django.contrib import admin
from .models import BlockchainData

@admin.register(BlockchainData)
class BlockchainDataAdmin(admin.ModelAdmin):
    list_display = ['network', 'block_height', 'timestamp']
    list_filter = ['network']
    search_fields = ['network']
