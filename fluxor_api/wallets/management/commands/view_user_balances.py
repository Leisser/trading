"""
Management command to view all user balances
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wallets.models import MultiCurrencyWallet, CryptoBalance
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'View all user cryptocurrency balances'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Filter by specific user email',
        )
        parser.add_argument(
            '--show-zero',
            action='store_true',
            help='Show zero balances',
        )

    def handle(self, *args, **options):
        email_filter = options.get('email')
        show_zero = options.get('show_zero', False)
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(self.style.SUCCESS('  USER CRYPTOCURRENCY BALANCES'))
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write('')
        
        # Get wallets
        wallets = MultiCurrencyWallet.objects.select_related('user').prefetch_related('balances__cryptocurrency')
        
        if email_filter:
            wallets = wallets.filter(user__email=email_filter)
        
        if wallets.count() == 0:
            self.stdout.write(self.style.WARNING('No multi-currency wallets found'))
            self.stdout.write('')
            self.stdout.write('Users need to access the wallet page to create their multi-currency wallet.')
            return
        
        total_users = wallets.count()
        total_value_usd = Decimal('0')
        
        for wallet in wallets:
            user = wallet.user
            balances = wallet.balances.all()
            
            if not show_zero:
                balances = [b for b in balances if b.balance > 0]
            
            wallet_total_usd = wallet.get_total_balance_usd()
            total_value_usd += wallet_total_usd
            
            # User header
            self.stdout.write(self.style.HTTP_INFO(f'\n👤 {user.email}'))
            self.stdout.write(f'   Wallet: {wallet.wallet_address}')
            self.stdout.write(f'   Total Value: ${wallet_total_usd:,.2f} USD')
            self.stdout.write(f'   Assets: {len(balances)}')
            self.stdout.write('')
            
            if not balances:
                self.stdout.write(self.style.WARNING('   No balances'))
            else:
                # Header
                self.stdout.write(f'   {"Cryptocurrency":<20} {"Balance":<20} {"USD Value":<15} {"Available":<15}')
                self.stdout.write(f'   {"-" * 70}')
                
                # Balances
                for balance in balances:
                    crypto_display = f'{balance.cryptocurrency.name} ({balance.cryptocurrency.symbol})'
                    balance_display = f'{balance.balance:.8f}'
                    usd_display = f'${balance.balance_usd:,.2f}'
                    available_display = f'{balance.available_balance:.8f}'
                    
                    self.stdout.write(
                        f'   {crypto_display:<20} {balance_display:<20} {usd_display:<15} {available_display:<15}'
                    )
            
            self.stdout.write('')
        
        # Summary
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(self.style.SUCCESS(f'  SUMMARY'))
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(f'Total Users: {total_users}')
        self.stdout.write(f'Total Platform Value: ${total_value_usd:,.2f} USD')
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write('')

