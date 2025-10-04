from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from decimal import Decimal
import json

from .models import (
    Cryptocurrency, CryptoWallet, CryptoSwap, CryptoPayment,
    Notification, Wallet, Trade, TradingSignal, Deposit, Withdrawal
)
from .serializers import (
    CryptoWalletSerializer, CryptoSwapSerializer, CryptoPaymentSerializer,
    ExecuteSwapSerializer, CreatePaymentSerializer, SwapQuoteSerializer,
    WalletBalanceSerializer, CryptocurrencySerializer, WalletSerializer,
    TradeSerializer, TradingSignalSerializer, DepositSerializer,
    WithdrawalSerializer, ExecuteTradeSerializer, PriceFeedSerializer,
    TradingSignalRequestSerializer, NotificationSerializer
)
from .crypto_services import (
    CryptoWalletService, CryptoSwapService, CryptoPaymentService,
    CryptoPriceService
)


class CryptoWalletListView(generics.ListCreateAPIView):
    """List and create crypto wallets"""
    
    serializer_class = CryptoWalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CryptoWallet.objects.filter(user=self.request.user, is_active=True)
    
    def perform_create(self, serializer):
        wallet_type = serializer.validated_data['wallet_type']
        
        # Generate wallet based on type
        if wallet_type == 'ethereum':
            address, private_key = CryptoWalletService.generate_ethereum_wallet()
            encrypted_key = CryptoWalletService.encrypt_private_key(private_key)
        elif wallet_type == 'bitcoin':
            address, private_key = CryptoWalletService.generate_bitcoin_address()
            encrypted_key = CryptoWalletService.encrypt_private_key(private_key)
        else:
            # For other cryptocurrencies, generate a mock address
            address = f"{wallet_type}_{self.request.user.id}_{timezone.now().timestamp()}"
            encrypted_key = ""
        
        serializer.save(
            user=self.request.user,
            address=address,
            private_key_encrypted=encrypted_key
        )


class CryptoWalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, and delete crypto wallet"""
    
    serializer_class = CryptoWalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CryptoWallet.objects.filter(user=self.request.user)


class WalletBalanceView(APIView):
    """Get wallet balances with USD values"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        wallets = CryptoWallet.objects.filter(user=request.user, is_active=True)
        balances = []
        
        # Get all cryptocurrency symbols for price lookup
        symbols = [wallet.wallet_type.upper() for wallet in wallets]
        prices = CryptoPriceService.get_coingecko_prices(symbols)
        
        for wallet in wallets:
            # Get real balance for Ethereum
            if wallet.wallet_type == 'ethereum':
                balance = CryptoWalletService.get_ethereum_balance(wallet.address)
                wallet.balance = balance
                wallet.save()
            
            # Calculate USD value
            symbol = wallet.wallet_type.upper()
            price_usd = prices.get(symbol, 0)
            usd_value = wallet.balance * Decimal(str(price_usd))
            
            balances.append({
                'wallet_type': wallet.wallet_type,
                'address': wallet.address,
                'balance': wallet.balance,
                'usd_value': usd_value,
                'price_usd': price_usd
            })
        
        return Response(balances)


class CryptoSwapListView(generics.ListCreateAPIView):
    """List and create crypto swaps"""
    
    serializer_class = CryptoSwapSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CryptoSwap.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CryptoSwapDetailView(generics.RetrieveAPIView):
    """Get crypto swap details"""
    
    serializer_class = CryptoSwapSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CryptoSwap.objects.filter(user=self.request.user)


class SwapQuoteView(APIView):
    """Get swap quote"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ExecuteSwapSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Get cryptocurrencies
            try:
                from_crypto = Cryptocurrency.objects.get(id=data['from_cryptocurrency_id'])
                to_crypto = Cryptocurrency.objects.get(id=data['to_cryptocurrency_id'])
            except Cryptocurrency.DoesNotExist:
                return Response({'error': 'Cryptocurrency not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
            
            # Get swap quote
            quote = CryptoSwapService.get_swap_quote(
                from_crypto.symbol,
                to_crypto.symbol,
                data['from_amount']
            )
            
            if quote:
                return Response(quote)
            else:
                return Response({'error': 'Unable to get swap quote'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExecuteSwapView(APIView):
    """Execute a crypto swap"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ExecuteSwapSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Get cryptocurrencies
            try:
                from_crypto = Cryptocurrency.objects.get(id=data['from_cryptocurrency_id'])
                to_crypto = Cryptocurrency.objects.get(id=data['to_cryptocurrency_id'])
            except Cryptocurrency.DoesNotExist:
                return Response({'error': 'Cryptocurrency not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
            
            # Get swap quote
            quote = CryptoSwapService.get_swap_quote(
                from_crypto.symbol,
                to_crypto.symbol,
                data['from_amount']
            )
            
            if not quote:
                return Response({'error': 'Unable to get swap quote'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Execute swap
            result = CryptoSwapService.execute_swap(quote)
            
            if result['success']:
                # Create swap record
                swap = CryptoSwap.objects.create(
                    user=request.user,
                    from_cryptocurrency=from_crypto,
                    to_cryptocurrency=to_crypto,
                    from_amount=quote['from_amount'],
                    to_amount=quote['to_amount'],
                    exchange_rate=quote['exchange_rate'],
                    network_fee=quote['network_fee'],
                    transaction_hash=result['transaction_hash'],
                    status='completed',
                    executed_at=result['executed_at'],
                    swap_provider=quote['provider']
                )
                
                # Create notification
                Notification.objects.create(
                    user=request.user,
                    notification_type='swap',
                    title='Crypto Swap Completed',
                    message=f'Successfully swapped {quote["from_amount"]} {from_crypto.symbol} for {quote["to_amount"]} {to_crypto.symbol}',
                    data={'swap_id': swap.id}
                )
                
                return Response({
                    'status': 'Swap executed successfully',
                    'swap': CryptoSwapSerializer(swap).data
                })
            else:
                return Response({'error': result['error']}, 
                              status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CryptoPaymentListView(generics.ListCreateAPIView):
    """List and create crypto payments"""
    
    serializer_class = CryptoPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CryptoPayment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CryptoPaymentDetailView(generics.RetrieveAPIView):
    """Get crypto payment details"""
    
    serializer_class = CryptoPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CryptoPayment.objects.filter(user=self.request.user)


class CreatePaymentView(APIView):
    """Create a crypto payment"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Get cryptocurrency
            try:
                crypto = Cryptocurrency.objects.get(symbol=data['cryptocurrency'].upper())
            except Cryptocurrency.DoesNotExist:
                return Response({'error': 'Cryptocurrency not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
            
            # Create payment
            payment_data = CryptoPaymentService.create_coinbase_payment(
                data['amount_usd'],
                crypto.symbol
            )
            
            if payment_data:
                payment = CryptoPayment.objects.create(
                    user=request.user,
                    amount_usd=data['amount_usd'],
                    amount_crypto=payment_data['amount_crypto'],
                    cryptocurrency=crypto,
                    payment_provider='coinbase',
                    provider_payment_id=payment_data['payment_id'],
                    payment_url=payment_data['payment_url'],
                    wallet_address=payment_data['wallet_address'],
                    expires_at=payment_data['expires_at'],
                    status=payment_data['status']
                )
                
                return Response({
                    'status': 'Payment created successfully',
                    'payment': CryptoPaymentSerializer(payment).data
                })
            else:
                return Response({'error': 'Unable to create payment'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_payment(request):
    """Verify a crypto payment"""
    payment_id = request.data.get('payment_id')
    transaction_hash = request.data.get('transaction_hash')
    
    if not payment_id or not transaction_hash:
        return Response({'error': 'Payment ID and transaction hash required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        payment = CryptoPayment.objects.get(
            payment_id=payment_id,
            user=request.user
        )
        
        # Verify payment
        is_verified = CryptoPaymentService.verify_payment(payment_id, transaction_hash)
        
        if is_verified:
            payment.status = 'confirmed'
            payment.transaction_hash = transaction_hash
            payment.confirmed_at = timezone.now()
            payment.save()
            
            # Create notification
            Notification.objects.create(
                user=request.user,
                notification_type='payment',
                title='Payment Confirmed',
                message=f'Your payment of {payment.amount_usd} USD has been confirmed',
                data={'payment_id': payment.payment_id}
            )
            
            return Response({'status': 'Payment verified successfully'})
        else:
            return Response({'error': 'Payment verification failed'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    except CryptoPayment.DoesNotExist:
        return Response({'error': 'Payment not found'}, 
                       status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_supported_tokens(request):
    """Get list of supported tokens for swaps"""
    tokens = Cryptocurrency.objects.filter(is_active=True)
    return Response([{
        'id': token.id,
        'symbol': token.symbol,
        'name': token.name,
        'current_price': token.current_price
    } for token in tokens])


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_swap_pairs(request):
    """Get available swap pairs"""
    # Define supported swap pairs
    pairs = [
        {'from': 'BTC', 'to': 'ETH'},
        {'from': 'BTC', 'to': 'SOL'},
        {'from': 'BTC', 'to': 'ADA'},
        {'from': 'BTC', 'to': 'DOT'},
        {'from': 'BTC', 'to': 'LINK'},
        {'from': 'ETH', 'to': 'BTC'},
        {'from': 'ETH', 'to': 'SOL'},
        {'from': 'ETH', 'to': 'ADA'},
        {'from': 'ETH', 'to': 'DOT'},
        {'from': 'ETH', 'to': 'LINK'},
        {'from': 'SOL', 'to': 'BTC'},
        {'from': 'SOL', 'to': 'ETH'},
        {'from': 'SOL', 'to': 'ADA'},
        {'from': 'SOL', 'to': 'DOT'},
        {'from': 'SOL', 'to': 'LINK'},
        {'from': 'ADA', 'to': 'BTC'},
        {'from': 'ADA', 'to': 'ETH'},
        {'from': 'ADA', 'to': 'SOL'},
        {'from': 'ADA', 'to': 'DOT'},
        {'from': 'ADA', 'to': 'LINK'},
        {'from': 'DOT', 'to': 'BTC'},
        {'from': 'DOT', 'to': 'ETH'},
        {'from': 'DOT', 'to': 'SOL'},
        {'from': 'DOT', 'to': 'ADA'},
        {'from': 'DOT', 'to': 'LINK'},
        {'from': 'LINK', 'to': 'BTC'},
        {'from': 'LINK', 'to': 'ETH'},
        {'from': 'LINK', 'to': 'SOL'},
        {'from': 'LINK', 'to': 'ADA'},
        {'from': 'LINK', 'to': 'DOT'},
    ]
    
    return Response(pairs)


# Additional views from fluxor_backend
class CryptocurrencyListView(generics.ListAPIView):
    """List all cryptocurrencies"""
    
    queryset = Cryptocurrency.objects.filter(is_active=True)
    serializer_class = CryptocurrencySerializer
    permission_classes = [permissions.AllowAny]


class CryptocurrencyDetailView(generics.RetrieveAPIView):
    """Get cryptocurrency details"""
    
    queryset = Cryptocurrency.objects.filter(is_active=True)
    serializer_class = CryptocurrencySerializer
    permission_classes = [permissions.AllowAny]


class WalletView(APIView):
    """Get user wallet"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(
            user=request.user,
            defaults={
                'address': f"wallet_{request.user.id}_{timezone.now().timestamp()}",
                'balance': Decimal('0.00000000'),
                'label': 'Main Wallet'
            }
        )
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class ExecuteTradeView(APIView):
    """Execute a trade"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ExecuteTradeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Get cryptocurrency
            try:
                crypto = Cryptocurrency.objects.get(id=data['cryptocurrency_id'])
            except Cryptocurrency.DoesNotExist:
                return Response({'error': 'Cryptocurrency not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
            
            # Get user wallet
            wallet, created = Wallet.objects.get_or_create(
                user=request.user,
                defaults={
                    'address': f"wallet_{request.user.id}_{timezone.now().timestamp()}",
                    'balance': Decimal('0.00000000'),
                    'label': 'Main Wallet'
                }
            )
            
            # Calculate trade details
            amount = data['amount']
            leverage = data['leverage']
            trade_type = data['trade_type']
            current_price = crypto.current_price
            
            # Calculate total value
            total_value = amount * current_price
            
            # Check if user has enough balance (simplified check)
            if trade_type == 'buy' and wallet.balance < amount:
                return Response({'error': 'Insufficient balance'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Create trade
            trade = Trade.objects.create(
                user=request.user,
                cryptocurrency=crypto,
                trade_type=trade_type,
                amount=amount,
                price=current_price,
                total_value=total_value,
                leverage=leverage,
                status='executed',
                executed_at=timezone.now()
            )
            
            # Update wallet balance (simplified)
            if trade_type == 'buy':
                wallet.balance -= amount
            else:
                wallet.balance += amount
            wallet.save()
            
            # Create notification
            Notification.objects.create(
                user=request.user,
                notification_type='trade',
                title=f'{trade_type.title()} Order Executed',
                message=f'Your {trade_type} order for {amount} {crypto.symbol} has been executed at ${current_price}',
                data={'trade_id': trade.id}
            )
            
            return Response({
                'status': 'Trade executed (simulated)',
                'trade': TradeSerializer(trade).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PriceFeedView(APIView):
    """Get current price feed"""
    
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Get latest price data for all active cryptocurrencies
        cryptocurrencies = Cryptocurrency.objects.filter(is_active=True)
        price_data = []
        
        for crypto in cryptocurrencies:
            # In a real app, you would fetch this from external APIs
            # For demo purposes, we'll generate mock data
            import random
            mock_price = Decimal(str(random.uniform(20000, 50000)))
            mock_volume = Decimal(str(random.uniform(1000000, 5000000)))
            mock_change = Decimal(str(random.uniform(-10, 10)))
            
            price_data.append({
                'symbol': crypto.symbol,
                'price': mock_price,
                'volume': mock_volume,
                'change_24h': mock_change,
                'timestamp': timezone.now()
            })
        
        return Response(price_data)


class TradingSignalView(APIView):
    """Get trading signals"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get latest trading signals
        signals = TradingSignal.objects.filter(is_active=True).order_by('-created_at')[:10]
        serializer = TradingSignalSerializer(signals, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TradingSignalRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            try:
                crypto = Cryptocurrency.objects.get(id=data['cryptocurrency_id'])
            except Cryptocurrency.DoesNotExist:
                return Response({'error': 'Cryptocurrency not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
            
            # Generate mock trading signal
            import random
            signal_types = ['buy', 'sell', 'hold']
            signal_type = random.choice(signal_types)
            confidence = Decimal(str(random.uniform(50, 95)))
            
            # Calculate mock indicators
            indicators = {
                'rsi': random.uniform(30, 70),
                'macd': random.uniform(-2, 2),
                'bollinger_bands': {
                    'upper': float(crypto.current_price * Decimal('1.05')),
                    'middle': float(crypto.current_price),
                    'lower': float(crypto.current_price * Decimal('0.95'))
                }
            }
            
            signal = TradingSignal.objects.create(
                cryptocurrency=crypto,
                signal_type=signal_type,
                confidence=confidence,
                reasoning=f"Generated signal based on technical analysis for {crypto.symbol}",
                indicators=indicators
            )
            
            return Response(TradingSignalSerializer(signal).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositListView(generics.ListCreateAPIView):
    """List and create deposits"""
    
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WithdrawalListView(generics.ListCreateAPIView):
    """List and create withdrawals"""
    
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Withdrawal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationListView(generics.ListAPIView):
    """List user notifications"""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationDetailView(generics.RetrieveUpdateAPIView):
    """Get and update notification"""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def check_deposits(request):
    """Check for new deposits"""
    # In a real app, this would check blockchain for new transactions
    # For demo purposes, we'll just return a success message
    return Response({'message': 'Deposit check completed'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def request_withdrawal(request):
    """Request a withdrawal"""
    amount = request.data.get('amount')
    to_address = request.data.get('to_address')
    
    if not amount or not to_address:
        return Response({'error': 'Amount and address are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Get user wallet
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        return Response({'error': 'Wallet not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Check balance
    if wallet.balance < Decimal(amount):
        return Response({'error': 'Insufficient balance'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Get default cryptocurrency (BTC for demo)
    crypto, created = Cryptocurrency.objects.get_or_create(
        symbol='BTC',
        defaults={
            'name': 'Bitcoin',
            'current_price': Decimal('45000.00')
        }
    )
    
    # Create withdrawal
    withdrawal = Withdrawal.objects.create(
        user=request.user,
        amount=amount,
        cryptocurrency=crypto,
        to_address=to_address,
        status='pending'
    )
    
    return Response({
        'message': 'Withdrawal request submitted',
        'withdrawal': WithdrawalSerializer(withdrawal).data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_trading_stats(request):
    """Get user trading statistics"""
    user = request.user
    
    # Get user profile
    profile, created = user.profile_set.get_or_create()
    
    # Get recent trades
    recent_trades = Trade.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Calculate basic stats
    total_trades = Trade.objects.filter(user=user).count()
    successful_trades = Trade.objects.filter(user=user, pnl__gt=0).count()
    total_volume = sum(trade.total_value for trade in Trade.objects.filter(user=user))
    
    return Response({
        'total_trades': total_trades,
        'successful_trades': successful_trades,
        'total_volume': total_volume,
        'win_rate': (successful_trades / total_trades * 100) if total_trades > 0 else 0,
        'recent_trades': TradeSerializer(recent_trades, many=True).data
    })