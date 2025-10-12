"""
Management command to create sample deposit wallets
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from trades.models import DepositWallet, Cryptocurrency

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample deposit wallets for different cryptocurrencies'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating deposit wallets...')
        
        # Get or create admin user for wallet creation
        admin_user, created = User.objects.get_or_create(
            email='admin@fluxor.pro',
            defaults={
                'username': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_user.email}'))
        
        # Sample deposit wallets data
        wallets_data = [
            {
                'crypto_symbol': 'BTC',
                'crypto_name': 'Bitcoin',
                'wallet_name': 'Main Bitcoin Wallet',
                'wallet_address': 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
                'is_primary': True,
            },
            {
                'crypto_symbol': 'ETH',
                'crypto_name': 'Ethereum',
                'wallet_name': 'Primary Ethereum Wallet',
                'wallet_address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
                'is_primary': True,
            },
            {
                'crypto_symbol': 'USDT',
                'crypto_name': 'Tether',
                'wallet_name': 'USDT (ERC-20) Wallet',
                'wallet_address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
                'is_primary': True,
            },
            {
                'crypto_symbol': 'USDC',
                'crypto_name': 'USD Coin',
                'wallet_name': 'USDC (ERC-20) Wallet',
                'wallet_address': '0x8e870d5a0e1b0a5b7c2c0e9c8c3e2e9c8e870d5a',
                'is_primary': True,
            },
            {
                'crypto_symbol': 'SOL',
                'crypto_name': 'Solana',
                'wallet_name': 'Solana Main Wallet',
                'wallet_address': 'DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK',
                'is_primary': True,
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for wallet_data in wallets_data:
            # Get or create cryptocurrency
            cryptocurrency, crypto_created = Cryptocurrency.objects.get_or_create(
                symbol=wallet_data['crypto_symbol'],
                defaults={
                    'name': wallet_data['crypto_name'],
                    'current_price': 0,
                    'is_active': True,
                    'is_tradeable': True,
                }
            )
            
            if crypto_created:
                self.stdout.write(self.style.SUCCESS(f'Created cryptocurrency: {cryptocurrency.symbol}'))
            
            # Create or update deposit wallet
            deposit_wallet, wallet_created = DepositWallet.objects.update_or_create(
                wallet_address=wallet_data['wallet_address'],
                defaults={
                    'cryptocurrency': cryptocurrency,
                    'wallet_name': wallet_data['wallet_name'],
                    'is_active': True,
                    'is_primary': wallet_data['is_primary'],
                    'created_by': admin_user,
                    'current_balance': 0,
                    'total_received': 0,
                    'total_confirmed': 0,
                    'min_confirmation_blocks': 3,
                }
            )
            
            if wallet_created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Created: {deposit_wallet.wallet_name} ({deposit_wallet.wallet_address[:20]}...)'
                ))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(
                    f'Updated: {deposit_wallet.wallet_name}'
                ))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'Summary:'))
        self.stdout.write(self.style.SUCCESS(f'  Deposit wallets created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'  Deposit wallets updated: {updated_count}'))
        self.stdout.write(self.style.SUCCESS(f'  Total deposit wallets: {DepositWallet.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

