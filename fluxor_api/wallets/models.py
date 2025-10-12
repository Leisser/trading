from django.db import models
from django.contrib.auth import get_user_model
from trades.models import Cryptocurrency

User = get_user_model()

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wallets')
    address = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user']

    def __str__(self):
        return f"{self.user.email} - {self.address}"


class MultiCurrencyWallet(models.Model):
    """Multi-currency wallet for holding different cryptocurrencies"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='multi_currency_wallet')
    wallet_address = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Multi-Currency Wallet"
    
    def get_total_balance_usd(self):
        """Calculate total balance in USD across all cryptocurrencies"""
        total = 0
        for balance in self.balances.all():
            total += balance.balance * balance.cryptocurrency.current_price
        return total


class CryptoBalance(models.Model):
    """Individual cryptocurrency balance within a multi-currency wallet"""
    wallet = models.ForeignKey(MultiCurrencyWallet, on_delete=models.CASCADE, related_name='balances')
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    locked_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)  # For pending orders
    
    # Statistics
    total_deposited = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    total_withdrawn = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['wallet', 'cryptocurrency']
        ordering = ['-balance']

    def __str__(self):
        return f"{self.wallet.user.email} - {self.cryptocurrency.symbol}: {self.balance}"
    
    @property
    def available_balance(self):
        """Available balance (total - locked)"""
        return self.balance - self.locked_balance
    
    @property
    def balance_usd(self):
        """Balance in USD"""
        return self.balance * self.cryptocurrency.current_price
