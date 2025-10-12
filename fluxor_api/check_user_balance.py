#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluxor_api.settings')
django.setup()

from accounts.models import User
from wallets.models import Wallet, MultiCurrencyWallet, CryptoBalance

# Get first user (or all users)
users = User.objects.all()

print("=" * 80)
print("USER BALANCES")
print("=" * 80)

for user in users[:5]:  # Show first 5 users
    print(f"\nUser: {user.email}")
    print(f"User ID: {user.id}")
    
    # Check old Wallet model
    try:
        wallet = Wallet.objects.get(user=user)
        print(f"  Old Wallet Balance: ${wallet.balance}")
    except Wallet.DoesNotExist:
        print(f"  Old Wallet: Not found")
    
    # Check MultiCurrencyWallet
    try:
        mcw = MultiCurrencyWallet.objects.get(user=user)
        print(f"  Multi-Currency Wallet: {mcw.wallet_address}")
        print(f"  Total USD Balance: ${mcw.get_total_balance_usd():.2f}")
        
        # Show individual crypto balances
        balances = CryptoBalance.objects.filter(wallet=mcw)
        if balances.exists():
            print(f"  Crypto Balances:")
            for bal in balances:
                print(f"    {bal.cryptocurrency.symbol}: {bal.balance} (${bal.get_usd_value():.2f})")
        else:
            print(f"  Crypto Balances: None")
            
    except MultiCurrencyWallet.DoesNotExist:
        print(f"  Multi-Currency Wallet: Not found")
    
    print("-" * 80)

print(f"\nTotal users: {User.objects.count()}")

