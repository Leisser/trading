from django.contrib import admin
from .models import Wallet

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'balance']
    list_filter = ['balance']
    search_fields = ['user__email', 'address']
