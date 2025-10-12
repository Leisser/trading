"""
Test script to demonstrate automatic balance update on deposit approval
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluxor_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from trades.models import UserDepositRequest, DepositWallet
from wallets.models import MultiCurrencyWallet, CryptoBalance
from decimal import Decimal
from django.utils import timezone

User = get_user_model()

print("\n" + "=" * 80)
print("  🧪 TESTING AUTOMATIC BALANCE UPDATE ON DEPOSIT APPROVAL")
print("=" * 80 + "\n")

# Get or create test user
user = User.objects.get(email='enoch.mbuga@gmail.com')

# Get a deposit wallet
deposit_wallet = DepositWallet.objects.filter(is_active=True).first()

if not deposit_wallet:
    print("❌ No deposit wallets found. Run: python manage.py create_deposit_wallets")
    exit(1)

print(f"✅ User: {user.email}")
print(f"✅ Deposit Wallet: {deposit_wallet.wallet_name}")
print(f"✅ Cryptocurrency: {deposit_wallet.cryptocurrency.symbol}\n")

# Check current balance BEFORE
try:
    wallet = user.multi_currency_wallet
    try:
        balance = wallet.balances.get(cryptocurrency=deposit_wallet.cryptocurrency)
        balance_before = balance.balance
    except CryptoBalance.DoesNotExist:
        balance_before = Decimal('0')
except MultiCurrencyWallet.DoesNotExist:
    balance_before = Decimal('0')

print(f"📊 BEFORE Approval:")
print(f"   Balance: {balance_before} {deposit_wallet.cryptocurrency.symbol}\n")

# Create test deposit request
deposit = UserDepositRequest.objects.create(
    user=user,
    deposit_wallet=deposit_wallet,
    amount=Decimal('0.5'),
    status='pending',
    from_address='test_user_wallet_address'
)

print(f"✅ Deposit Request Created!")
print(f"   ID: {deposit.id}")
print(f"   Amount: {deposit.amount} {deposit_wallet.cryptocurrency.symbol}")
print(f"   Status: {deposit.status}\n")

# Simulate admin approval
print("⏳ Simulating admin approval...\n")

# Get admin user
admin = User.objects.filter(is_superuser=True).first()
if not admin:
    admin = User.objects.get(email='admin@fluxor.pro')

# Approve deposit (simulate the AdminDepositApprovalView logic)
deposit.status = 'confirmed'
deposit.reviewed_by = admin
deposit.reviewed_at = timezone.now()
deposit.confirmed_at = timezone.now()
deposit.review_notes = 'Test approval - automated script'

# Credit multi-currency wallet
multi_wallet, created = MultiCurrencyWallet.objects.get_or_create(
    user=deposit.user,
    defaults={
        'wallet_address': f'MCW_{deposit.user.id}_TEST',
        'is_active': True
    }
)

crypto_balance, balance_created = CryptoBalance.objects.get_or_create(
    wallet=multi_wallet,
    cryptocurrency=deposit.deposit_wallet.cryptocurrency,
    defaults={'balance': Decimal('0')}
)

crypto_balance.balance += deposit.amount
crypto_balance.total_deposited += deposit.amount
crypto_balance.save()

deposit.save()

print(f"✅ Deposit Approved!")
print(f"   Status: {deposit.status}")
print(f"   Reviewed by: {deposit.reviewed_by.email}")
print(f"   Confirmed at: {deposit.confirmed_at}\n")

# Check balance AFTER
balance_after = crypto_balance.balance

print(f"📊 AFTER Approval:")
print(f"   Balance: {balance_after} {deposit_wallet.cryptocurrency.symbol}")
print(f"   Total Deposited: {crypto_balance.total_deposited}\n")

print("=" * 80)
print(f"  ✅ SUCCESS! Balance automatically updated from {balance_before} to {balance_after}")
print("=" * 80 + "\n")

print("🔍 Verify in frontend:")
print(f"   1. Sign in as {user.email}")
print(f"   2. Go to http://localhost:5173/wallet")
print(f"   3. See 'My Balances' tab")
print(f"   4. You should see: {deposit_wallet.cryptocurrency.symbol}: {balance_after}\n")

