"""
Trade execution logic with balance validation and profit/loss tracking
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import Trade, Cryptocurrency
from wallets.models import MultiCurrencyWallet, CryptoBalance


class TradeExecutor:
    """
    Handles trade execution with proper balance management and profit/loss tracking
    """
    
    def __init__(self, user):
        self.user = user
        # Get or create multi-currency wallet
        import uuid
        self.wallet, created = MultiCurrencyWallet.objects.get_or_create(
            user=user,
            defaults={
                'wallet_address': f'MCW_{uuid.uuid4().hex[:16].upper()}',
                'is_active': True
            }
        )
    
    def execute_buy_order(self, cryptocurrency_symbol, amount, price, leverage=1):
        """
        Execute a buy order - PURE DEDUCTION MODEL
        - Deducts USD/USDT from wallet (margin + fee)
        - Does NOT add cryptocurrency to wallet
        - All trades cost money, never add to balance
        """
        try:
            cryptocurrency = Cryptocurrency.objects.get(symbol=cryptocurrency_symbol)
        except Cryptocurrency.DoesNotExist:
            raise ValidationError(f"Cryptocurrency {cryptocurrency_symbol} not found")
        
        # Calculate total cost (including leverage)
        total_cost = Decimal(amount) * Decimal(price)
        required_margin = total_cost / Decimal(leverage)
        trading_fee = total_cost * Decimal('0.001')  # 0.1% trading fee
        total_deduction = required_margin + trading_fee
        
        # Get or create USDT balance (assuming USDT as quote currency)
        try:
            usdt = Cryptocurrency.objects.get(symbol='USDT')
            usdt_balance, _ = CryptoBalance.objects.get_or_create(
                wallet=self.wallet,
                cryptocurrency=usdt,
                defaults={'balance': 0}
            )
        except Cryptocurrency.DoesNotExist:
            raise ValidationError("USDT not configured in system")
        
        # Check if user has sufficient balance
        if usdt_balance.available_balance < total_deduction:
            raise ValidationError(
                f"Insufficient balance. Required: {total_deduction} USDT, "
                f"Available: {usdt_balance.available_balance} USDT"
            )
        
        with transaction.atomic():
            # Deduct USDT from wallet (margin + fee)
            usdt_balance.balance -= total_deduction
            usdt_balance.save()
            
            # DO NOT add cryptocurrency to wallet - pure deduction system
            # crypto_balance is NOT modified
            
            # Create trade record
            trade = Trade.objects.create(
                user=self.user,
                cryptocurrency=cryptocurrency,
                trade_type='buy',
                amount=amount,
                price=price,
                total_value=total_cost,
                leverage=leverage,
                status='executed',
                pnl=-total_deduction,  # Negative PnL (cost of trade)
                fees=trading_fee,
                executed_at=timezone.now()
            )
            
            return trade
    
    def execute_sell_order(self, cryptocurrency_symbol, amount, price, leverage=1):
        """
        Execute a sell order - PURE DEDUCTION MODEL
        - Deducts trading fee from USDT balance
        - Does NOT add proceeds back to wallet
        - All trades cost money, never add to balance
        """
        try:
            cryptocurrency = Cryptocurrency.objects.get(symbol=cryptocurrency_symbol)
        except Cryptocurrency.DoesNotExist:
            raise ValidationError(f"Cryptocurrency {cryptocurrency_symbol} not found")
        
        # Calculate fee
        total_proceeds = Decimal(amount) * Decimal(price)
        trading_fee = total_proceeds * Decimal('0.001')  # 0.1% fee
        
        # Get or create USDT balance
        try:
            usdt = Cryptocurrency.objects.get(symbol='USDT')
            usdt_balance, _ = CryptoBalance.objects.get_or_create(
                wallet=self.wallet,
                cryptocurrency=usdt,
                defaults={'balance': 0}
            )
        except Cryptocurrency.DoesNotExist:
            raise ValidationError("USDT not configured in system")
        
        # Check if user has sufficient USDT for fee
        if usdt_balance.available_balance < trading_fee:
            raise ValidationError(
                f"Insufficient USDT balance for trading fee. Required: {trading_fee} USDT, "
                f"Available: {usdt_balance.available_balance} USDT"
            )
        
        with transaction.atomic():
            # Deduct trading fee from USDT balance (DO NOT add proceeds)
            usdt_balance.balance -= trading_fee
            usdt_balance.save()
            
            # Calculate PnL (negative - user loses the fee)
            actual_pnl = -trading_fee
            
            # Create trade record with profit/loss
            trade = Trade.objects.create(
                user=self.user,
                cryptocurrency=cryptocurrency,
                trade_type='sell',
                amount=amount,
                price=price,
                total_value=total_proceeds,
                leverage=leverage,
                status='executed',
                pnl=actual_pnl,
                fees=trading_fee,
                executed_at=timezone.now()
            )
            
            return trade
    
    def execute_swap(self, from_symbol, to_symbol, from_amount):
        """
        Execute a crypto-to-crypto swap
        - Deducts source cryptocurrency
        - Adds destination cryptocurrency
        - Calculates exchange rate
        """
        try:
            from_crypto = Cryptocurrency.objects.get(symbol=from_symbol)
            to_crypto = Cryptocurrency.objects.get(symbol=to_symbol)
        except Cryptocurrency.DoesNotExist as e:
            raise ValidationError(f"Cryptocurrency not found: {str(e)}")
        
        # Get source balance
        try:
            from_balance = CryptoBalance.objects.get(
                wallet=self.wallet,
                cryptocurrency=from_crypto
            )
        except CryptoBalance.DoesNotExist:
            raise ValidationError(f"No {from_symbol} balance found")
        
        # Check sufficient balance
        if from_balance.available_balance < Decimal(from_amount):
            raise ValidationError(
                f"Insufficient balance. Required: {from_amount} {from_symbol}, "
                f"Available: {from_balance.available_balance} {from_symbol}"
            )
        
        # Calculate exchange rate based on current prices
        from_usd_value = Decimal(from_amount) * from_crypto.current_price
        to_amount = from_usd_value / to_crypto.current_price
        swap_fee = to_amount * Decimal('0.003')  # 0.3% swap fee
        to_amount_after_fee = to_amount - swap_fee
        
        with transaction.atomic():
            # Deduct source cryptocurrency
            from_balance.balance -= Decimal(from_amount)
            from_balance.save()
            
            # Add destination cryptocurrency
            to_balance, _ = CryptoBalance.objects.get_or_create(
                wallet=self.wallet,
                cryptocurrency=to_crypto,
                defaults={'balance': 0}
            )
            to_balance.balance += to_amount_after_fee
            to_balance.save()
            
            # Create trade record (marked as swap)
            trade = Trade.objects.create(
                user=self.user,
                cryptocurrency=from_crypto,
                trade_type='swap',
                amount=from_amount,
                price=from_crypto.current_price,
                total_value=from_usd_value,
                leverage=1,
                status='executed',
                pnl=Decimal('0'),
                fees=swap_fee * to_crypto.current_price,
                executed_at=timezone.now(),
                notes=f"Swapped {from_amount} {from_symbol} to {to_amount_after_fee} {to_symbol}"
            )
            
            return trade
    
    def get_available_balance(self, cryptocurrency_symbol):
        """Get available balance for a specific cryptocurrency"""
        try:
            cryptocurrency = Cryptocurrency.objects.get(symbol=cryptocurrency_symbol)
            balance = CryptoBalance.objects.get(
                wallet=self.wallet,
                cryptocurrency=cryptocurrency
            )
            return balance.available_balance
        except (Cryptocurrency.DoesNotExist, CryptoBalance.DoesNotExist):
            return Decimal('0')
    
    def calculate_total_pnl(self):
        """Calculate total profit/loss across all trades"""
        from django.db.models import Sum
        
        total_pnl = Trade.objects.filter(
            user=self.user,
            status='executed'
        ).aggregate(
            total=Sum('pnl')
        )['total'] or Decimal('0')
        
        return total_pnl

