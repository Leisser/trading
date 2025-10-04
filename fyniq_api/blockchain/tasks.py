from celery import shared_task
from django.utils import timezone
from wallets.models import BTCWallet, WithdrawalRequest
from wallets.services import WalletService
from .models import BlockchainMonitor

@shared_task
def check_all_deposits():
    """Check for new deposits across all user wallets"""
    wallet_service = WalletService()
    wallets = BTCWallet.objects.filter(wallet_type='user', is_active=True)
    
    total_new_deposits = 0
    for wallet in wallets:
        try:
            new_deposits = wallet_service.check_deposits(wallet)
            total_new_deposits += len(new_deposits)
        except Exception as e:
            print(f"Error checking deposits for wallet {wallet.address}: {str(e)}")
    
    return f"Checked {len(wallets)} wallets, found {total_new_deposits} new deposits"

@shared_task
def process_pending_withdrawals():
    """Process all pending withdrawal requests"""
    wallet_service = WalletService()
    pending_withdrawals = WithdrawalRequest.objects.filter(status='approved')
    
    processed_count = 0
    for withdrawal in pending_withdrawals:
        try:
            wallet_service.process_withdrawal(withdrawal)
            processed_count += 1
        except Exception as e:
            print(f"Error processing withdrawal {withdrawal.id}: {str(e)}")
            withdrawal.status = 'failed'
            withdrawal.notes = f"Processing failed: {str(e)}"
            withdrawal.save()
    
    return f"Processed {processed_count} withdrawals"

@shared_task
def update_wallet_balances():
    """Update balances for all wallets"""
    wallet_service = WalletService()
    wallets = BTCWallet.objects.filter(is_active=True)
    
    updated_count = 0
    for wallet in wallets:
        try:
            wallet_service.update_wallet_balance(wallet)
            updated_count += 1
        except Exception as e:
            print(f"Error updating balance for wallet {wallet.address}: {str(e)}")
    
    return f"Updated {updated_count} wallet balances"

@shared_task
def monitor_blockchain_health():
    """Monitor blockchain connection and health"""
    try:
        wallet_service = WalletService()
        # Test connection by getting a sample balance
        test_wallet = BTCWallet.objects.filter(wallet_type='company').first()
        if test_wallet:
            wallet_service.get_wallet_balance(test_wallet)
        
        BlockchainMonitor.objects.create(
            status='healthy',
            message='Blockchain connection successful'
        )
        return "Blockchain health check passed"
    except Exception as e:
        BlockchainMonitor.objects.create(
            status='error',
            message=f'Blockchain connection failed: {str(e)}'
        )
        return f"Blockchain health check failed: {str(e)}" 