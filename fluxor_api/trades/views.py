"""
Views for trades app - Cryptocurrency management and trading operations.
"""
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Sum
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from decimal import Decimal
import json
from .permissions import IsSuperuserOrStaff


class CryptocurrencyFilterSet(FilterSet):
    """Custom filter set for Cryptocurrency to handle JSONField properly"""
    class Meta:
        model = Cryptocurrency
        fields = ['is_featured', 'is_stablecoin', 'is_active']

from .models import (
    Cryptocurrency, CryptoWallet, Wallet, Trade, Deposit, Withdrawal,
    CryptoPayment, CryptoIndex, IndexComponent, CryptoInvestment,
    ProfitLossScenario, DepositWallet, UserDepositRequest
)
from .serializers import (
    CryptocurrencySerializer, CryptocurrencyListSerializer, CryptocurrencyDetailSerializer,
    CryptoWalletSerializer, WalletSerializer, TradeSerializer, DepositSerializer,
    WithdrawalSerializer, CryptoPaymentSerializer, CryptoIndexSerializer,
    IndexComponentSerializer, CryptoInvestmentSerializer, ProfitLossScenarioSerializer,
    DepositWalletSerializer, UserDepositRequestSerializer
)
from .trade_execution import TradeExecutor
from .biased_trade_executor import BiasedTradeExecutor
from wallets.models import MultiCurrencyWallet, CryptoBalance
from django.db import transaction as db_transaction


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination for cryptocurrency lists"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class CryptocurrencyListView(generics.ListAPIView):
    """
    List all cryptocurrencies with filtering and search capabilities.
    
    Query parameters:
    - search: Search by symbol or name
    - category: Filter by category (custom filter in get_queryset)
    - is_featured: Filter featured cryptocurrencies
    - is_stablecoin: Filter stablecoins
    - is_active: Filter active cryptocurrencies
    - min_market_cap: Minimum market cap filter
    - max_market_cap: Maximum market cap filter
    - ordering: Order by field (rank, market_cap, price_change_24h, etc.)
    """
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencyListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CryptocurrencyFilterSet  # Use custom filter set to avoid JSONField issues
    search_fields = ['symbol', 'name']
    ordering_fields = ['rank', 'market_cap', 'current_price', 'price_change_24h', 'volume_24h']
    ordering = ['rank']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Custom filters
        min_market_cap = self.request.query_params.get('min_market_cap')
        max_market_cap = self.request.query_params.get('max_market_cap')
        category = self.request.query_params.get('category')
        
        if min_market_cap:
            try:
                queryset = queryset.filter(market_cap__gte=Decimal(min_market_cap))
            except (ValueError, TypeError):
                pass
        
        if max_market_cap:
            try:
                queryset = queryset.filter(market_cap__lte=Decimal(max_market_cap))
            except (ValueError, TypeError):
                pass
        
        if category:
            queryset = queryset.filter(categories__contains=[category])
        
        return queryset


class CryptocurrencyDetailView(generics.RetrieveAPIView):
    """Get detailed information about a specific cryptocurrency"""
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencyDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'symbol'


class CryptocurrencyCreateView(generics.CreateAPIView):
    """Create a new cryptocurrency (Admin only)"""
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer
    permission_classes = [permissions.IsAdminUser]


class CryptocurrencyUpdateView(generics.UpdateAPIView):
    """Update cryptocurrency information (Admin only)"""
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'symbol'


class CryptocurrencyDeleteView(generics.DestroyAPIView):
    """Delete a cryptocurrency (Admin only)"""
    queryset = Cryptocurrency.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'symbol'


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_top_cryptocurrencies(request):
    """
    Get top N cryptocurrencies by market cap.
    
    Query parameters:
    - limit: Number of cryptocurrencies to return (default: 10, max: 100)
    - category: Filter by category
    - exclude_stablecoins: Exclude stablecoins from results
    """
    try:
        limit = min(int(request.GET.get('limit', 10)), 100)
        category = request.GET.get('category')
        exclude_stablecoins = request.GET.get('exclude_stablecoins', 'false').lower() == 'true'
        
        queryset = Cryptocurrency.objects.filter(is_active=True)
        
        if exclude_stablecoins:
            queryset = queryset.filter(is_stablecoin=False)
        
        if category:
            queryset = queryset.filter(categories__contains=[category])
        
        cryptocurrencies = queryset.order_by('rank')[:limit]
        serializer = CryptocurrencyListSerializer(cryptocurrencies, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except ValueError:
        return Response(
            {'error': 'Invalid limit parameter'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_featured_cryptocurrencies(request):
    """Get featured cryptocurrencies"""
    cryptocurrencies = Cryptocurrency.objects.filter(
        is_active=True, 
        is_featured=True
    ).order_by('rank')
    
    serializer = CryptocurrencyListSerializer(cryptocurrencies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_stablecoins(request):
    """Get all stablecoins"""
    stablecoins = Cryptocurrency.objects.filter(
        is_active=True, 
        is_stablecoin=True
    ).order_by('rank')
    
    serializer = CryptocurrencyListSerializer(stablecoins, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_cryptocurrency_categories(request):
    """Get all available cryptocurrency categories"""
    categories = set()
    for crypto in Cryptocurrency.objects.filter(is_active=True):
        categories.update(crypto.categories or [])
    
    return Response(sorted(list(categories)), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_cryptocurrencies(request):
    """
    Search cryptocurrencies by symbol or name.
    
    Query parameters:
    - q: Search query (required)
    - limit: Maximum number of results (default: 20)
    """
    query = request.GET.get('q', '').strip()
    if not query:
        return Response(
            {'error': 'Search query is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        limit = min(int(request.GET.get('limit', 20)), 50)
    except ValueError:
        limit = 20
    
    # Search by symbol (exact match) or name (partial match)
    cryptocurrencies = Cryptocurrency.objects.filter(
        Q(symbol__iexact=query) | Q(name__icontains=query),
        is_active=True
    ).order_by('rank')[:limit]
    
    serializer = CryptocurrencyListSerializer(cryptocurrencies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_cryptocurrency_stats(request):
    """Get overall cryptocurrency market statistics"""
    total_cryptocurrencies = Cryptocurrency.objects.filter(is_active=True).count()
    total_market_cap = Cryptocurrency.objects.filter(is_active=True).aggregate(
        total_market_cap=Sum('market_cap')
    )['total_market_cap'] or Decimal('0')
    
    total_volume_24h = Cryptocurrency.objects.filter(is_active=True).aggregate(
        total_volume=Sum('volume_24h')
    )['total_volume'] or Decimal('0')
    
    featured_count = Cryptocurrency.objects.filter(
        is_active=True, 
        is_featured=True
    ).count()
    
    stablecoin_count = Cryptocurrency.objects.filter(
        is_active=True, 
        is_stablecoin=True
    ).count()
    
    # Get top gainers and losers
    top_gainers = Cryptocurrency.objects.filter(
        is_active=True,
        price_change_24h__gt=0
    ).order_by('-price_change_24h')[:5]
    
    top_losers = Cryptocurrency.objects.filter(
        is_active=True,
        price_change_24h__lt=0
    ).order_by('price_change_24h')[:5]
    
    stats = {
        'total_cryptocurrencies': total_cryptocurrencies,
        'total_market_cap': total_market_cap,
        'total_volume_24h': total_volume_24h,
        'featured_count': featured_count,
        'stablecoin_count': stablecoin_count,
        'top_gainers': CryptocurrencyListSerializer(top_gainers, many=True).data,
        'top_losers': CryptocurrencyListSerializer(top_losers, many=True).data,
    }
    
    return Response(stats, status=status.HTTP_200_OK)


class CryptoWalletListView(generics.ListCreateAPIView):
    """List and create crypto wallets for authenticated users"""
    serializer_class = CryptoWalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CryptoWallet.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CryptoWalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a crypto wallet"""
    serializer_class = CryptoWalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CryptoWallet.objects.filter(user=self.request.user)


class TradeListView(generics.ListCreateAPIView):
    """List and create trades for authenticated users"""
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['cryptocurrency', 'trade_type', 'status']
    ordering_fields = ['created_at', 'amount', 'price', 'profit_loss']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TradeDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve or update a trade"""
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)


class DepositListView(generics.ListCreateAPIView):
    """List and create deposits for authenticated users"""
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['cryptocurrency', 'status']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WithdrawalListView(generics.ListCreateAPIView):
    """List and create withdrawals for authenticated users"""
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['cryptocurrency', 'status']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Withdrawal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CryptoIndexListView(generics.ListAPIView):
    """List all crypto indices"""
    queryset = CryptoIndex.objects.filter(is_active=True)
    serializer_class = CryptoIndexSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['index_type', 'is_tradeable']
    ordering_fields = ['name', 'current_value', 'price_change_24h']
    ordering = ['name']


class CryptoIndexDetailView(generics.RetrieveAPIView):
    """Get detailed information about a crypto index"""
    queryset = CryptoIndex.objects.all()
    serializer_class = CryptoIndexSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'symbol'


class CryptoInvestmentListView(generics.ListCreateAPIView):
    """List and create crypto investments for authenticated users"""
    serializer_class = CryptoInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['investment_type', 'status', 'crypto_index', 'cryptocurrency']
    ordering_fields = ['started_at', 'total_invested_usd', 'current_value_usd']
    ordering = ['-started_at']
    
    def get_queryset(self):
        return CryptoInvestment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CryptoInvestmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a crypto investment"""
    serializer_class = CryptoInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CryptoInvestment.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics"""
    try:
        from django.utils import timezone

        # Calculate various statistics
        total_users = request.user.__class__.objects.count()
        total_cryptocurrencies = Cryptocurrency.objects.filter(is_active=True).count()
        total_trades = Trade.objects.count()
        total_volume = Trade.objects.aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')

        # Wallet statistics
        pending_deposits = UserDepositRequest.objects.filter(status='pending').count()
        pending_withdrawals = Withdrawal.objects.filter(status='pending').count()
        
        # Calculate total balance in USD across all users' multi-currency wallets
        total_balance_usd = Decimal('0')
        from wallets.models import MultiCurrencyWallet
        for wallet in MultiCurrencyWallet.objects.filter(is_active=True):
            total_balance_usd += wallet.get_total_balance_usd()
        
        total_balance = total_balance_usd

        # Recent activity
        recent_trades = Trade.objects.order_by('-created_at')[:5]
        recent_trades_data = TradeSerializer(recent_trades, many=True).data

        # Top cryptocurrencies by market cap
        top_cryptos = Cryptocurrency.objects.filter(
            is_active=True
        ).order_by('-market_cap')[:10]
        top_cryptos_data = CryptocurrencyListSerializer(top_cryptos, many=True).data

        return Response({
            'total_users': total_users,
            'total_cryptocurrencies': total_cryptocurrencies,
            'total_trades': total_trades,
            'total_volume': total_volume,
            'total_balance': total_balance,
            'pending_deposits': pending_deposits,
            'pending_withdrawals': pending_withdrawals,
            'recent_trades': recent_trades_data,
            'top_cryptocurrencies': top_cryptos_data,
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsSuperuserOrStaff])
def admin_users_list(request):
    """Get all users with their balance information for admin"""
    try:
        from django.contrib.auth import get_user_model
        from wallets.models import MultiCurrencyWallet
        
        User = get_user_model()
        users = User.objects.all().order_by('-date_joined')
        
        users_data = []
        for user in users:
            try:
                wallet = user.multi_currency_wallet
                total_balance_usd = wallet.get_total_balance_usd()
            except MultiCurrencyWallet.DoesNotExist:
                total_balance_usd = Decimal('0')
            
            users_data.append({
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'total_balance_usd': float(total_balance_usd),
            })
        
        return Response({
            'users': users_data,
            'total_count': len(users_data),
            'total_balance_usd': sum(user['total_balance_usd'] for user in users_data)
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Admin Views for Wallet Management

class AdminDepositRequestListView(APIView):
    """Admin view to list all deposit requests"""
    permission_classes = [permissions.IsAuthenticated, IsSuperuserOrStaff]

    def get(self, request):
        try:
            deposits = UserDepositRequest.objects.all().order_by('-created_at')
            serializer = UserDepositRequestSerializer(deposits, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminDepositApprovalView(APIView):
    """Admin view to approve/reject deposit requests"""
    permission_classes = [permissions.IsAuthenticated, IsSuperuserOrStaff]

    def post(self, request, deposit_id):
        try:
            from django.utils import timezone
            from wallets.models import MultiCurrencyWallet, CryptoBalance
            import uuid

            deposit = get_object_or_404(UserDepositRequest, id=deposit_id)
            action = request.data.get('action')  # 'approve' or 'reject'
            admin_notes = request.data.get('admin_notes', '')

            if action == 'approve':
                deposit.status = 'confirmed'
                deposit.reviewed_by = request.user
                deposit.reviewed_at = timezone.now()
                deposit.confirmed_at = timezone.now()

                # Create a Deposit record for tracking
                deposit_record = Deposit.objects.create(
                    user=deposit.user,
                    amount=deposit.amount,
                    cryptocurrency=deposit.deposit_wallet.cryptocurrency,
                    deposit_wallet=deposit.deposit_wallet,
                    transaction_hash=deposit.transaction_hash,
                    wallet_address=deposit.deposit_wallet.wallet_address,
                    status='confirmed',
                    confirmed_at=timezone.now()
                )

                # Credit user's multi-currency wallet
                multi_wallet, created = MultiCurrencyWallet.objects.get_or_create(
                    user=deposit.user,
                    defaults={
                        'wallet_address': f'MCW_{uuid.uuid4().hex[:16].upper()}',
                        'is_active': True
                    }
                )

                # Get or create crypto balance for this cryptocurrency
                crypto_balance, balance_created = CryptoBalance.objects.get_or_create(
                    wallet=multi_wallet,
                    cryptocurrency=deposit.deposit_wallet.cryptocurrency,
                    defaults={'balance': Decimal('0')}
                )

                # Credit the balance
                crypto_balance.balance += deposit.amount
                crypto_balance.total_deposited += deposit.amount
                crypto_balance.save()

                # Also update legacy wallet for backward compatibility
                wallet, created = Wallet.objects.get_or_create(
                    user=deposit.user,
                    defaults={'address': f'wallet_{deposit.user.id}', 'balance': Decimal('0')}
                )
                wallet.balance += deposit.amount
                wallet.save()

                # Update deposit wallet statistics
                deposit.deposit_wallet.total_received += deposit.amount
                deposit.deposit_wallet.total_confirmed += deposit.amount
                deposit.deposit_wallet.current_balance += deposit.amount
                deposit.deposit_wallet.save()

            elif action == 'reject':
                deposit.status = 'rejected'
                deposit.reviewed_by = request.user
                deposit.reviewed_at = timezone.now()
            else:
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

            deposit.review_notes = admin_notes
            deposit.save()

            return Response({
                'message': f'Deposit {action}d successfully',
                'status': deposit.status,
                'deposit': UserDepositRequestSerializer(deposit).data
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminWithdrawalRequestListView(APIView):
    """Admin view to list all withdrawal requests"""
    permission_classes = [permissions.IsAuthenticated, IsSuperuserOrStaff]

    def get(self, request):
        try:
            withdrawals = Withdrawal.objects.all().order_by('-created_at')
            serializer = WithdrawalSerializer(withdrawals, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminWithdrawalApprovalView(APIView):
    """Admin view to approve/reject withdrawal requests"""
    permission_classes = [permissions.IsAuthenticated, IsSuperuserOrStaff]

    def post(self, request, withdrawal_id):
        try:
            from django.utils import timezone

            withdrawal = get_object_or_404(Withdrawal, id=withdrawal_id)
            action = request.data.get('action')  # 'approve' or 'reject'
            admin_notes = request.data.get('admin_notes', '')
            transaction_hash = request.data.get('transaction_hash', '')

            if action == 'approve':
                # Check if user has sufficient balance
                wallet = get_object_or_404(Wallet, user=withdrawal.user)
                if wallet.balance < withdrawal.amount:
                    return Response(
                        {'error': 'Insufficient balance'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                withdrawal.status = 'approved'
                withdrawal.approved_by = request.user
                withdrawal.approved_at = timezone.now()
                withdrawal.transaction_hash = transaction_hash

                # Deduct from user's wallet
                wallet.balance -= withdrawal.amount
                wallet.save()

            elif action == 'reject':
                withdrawal.status = 'rejected'
                withdrawal.approved_by = request.user
                withdrawal.approved_at = timezone.now()
            else:
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

            withdrawal.admin_notes = admin_notes
            withdrawal.save()

            return Response({
                'message': f'Withdrawal {action}d successfully',
                'status': withdrawal.status
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Trading API Views

class TradingPairListView(APIView):
    """List all available trading pairs"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            # Mock trading pairs data
            trading_pairs = [
                {
                    'id': 'BTC-USD',
                    'symbol': 'BTC/USD',
                    'base_currency': 'BTC',
                    'quote_currency': 'USD',
                    'current_price': 43250.50,
                    'price_change_24h': 2.45,
                    'volume_24h': 1250000,
                    'is_active': True
                },
                {
                    'id': 'ETH-USD',
                    'symbol': 'ETH/USD',
                    'base_currency': 'ETH',
                    'quote_currency': 'USD',
                    'current_price': 2650.75,
                    'price_change_24h': -1.23,
                    'volume_24h': 850000,
                    'is_active': True
                },
                {
                    'id': 'ADA-USD',
                    'symbol': 'ADA/USD',
                    'base_currency': 'ADA',
                    'quote_currency': 'USD',
                    'current_price': 0.485,
                    'price_change_24h': 5.67,
                    'volume_24h': 125000,
                    'is_active': True
                }
            ]
            return Response(trading_pairs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderBookView(APIView):
    """Get order book for a trading pair"""
    permission_classes = [permissions.AllowAny]

    def get(self, request, pair_id):
        try:
            # Mock order book data
            order_book = {
                'bids': [
                    {'price': 43245.50, 'amount': 0.5, 'total': 21622.75},
                    {'price': 43240.25, 'amount': 1.2, 'total': 51888.30},
                    {'price': 43235.00, 'amount': 0.8, 'total': 34588.00},
                    {'price': 43230.75, 'amount': 2.1, 'total': 90784.58},
                    {'price': 43225.50, 'amount': 0.3, 'total': 12967.65}
                ],
                'asks': [
                    {'price': 43255.75, 'amount': 0.7, 'total': 30279.03},
                    {'price': 43260.00, 'amount': 1.5, 'total': 64890.00},
                    {'price': 43265.25, 'amount': 0.9, 'total': 38938.73},
                    {'price': 43270.50, 'amount': 1.8, 'total': 77886.90},
                    {'price': 43275.75, 'amount': 0.4, 'total': 17310.30}
                ]
            }
            return Response(order_book)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlaceOrderView(APIView):
    """Place a trading order"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            trading_pair = request.data.get('trading_pair')
            order_type = request.data.get('order_type')  # 'market' or 'limit'
            side = request.data.get('side')  # 'buy' or 'sell'
            amount = Decimal(str(request.data.get('amount', 0)))
            price = Decimal(str(request.data.get('price', 0)))

            # Validate input
            if not all([trading_pair, order_type, side, amount]):
                return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

            if amount <= 0:
                return Response({'error': 'Amount must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)

            if order_type == 'limit' and price <= 0:
                return Response({'error': 'Price must be greater than 0 for limit orders'}, status=status.HTTP_400_BAD_REQUEST)

            # Check user balance for buy orders
            if side == 'buy':
                wallet = get_object_or_404(Wallet, user=request.user)
                required_amount = amount * price if order_type == 'limit' else amount * Decimal('43250')  # Mock current price

                if wallet.balance < required_amount:
                    return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

            # Create trade record
            trade = Trade.objects.create(
                user=request.user,
                cryptocurrency=trading_pair.split('-')[0],
                trade_type=side,
                amount=amount,
                price=price if order_type == 'limit' else Decimal('43250'),  # Mock current price
                status='pending'
            )

            return Response({
                'id': trade.id,
                'message': 'Order placed successfully',
                'status': 'pending'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserOrdersView(APIView):
    """Get user's trading orders"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            trades = Trade.objects.filter(user=request.user).order_by('-created_at')
            serializer = TradeSerializer(trades, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def execute_trade(request):
    """
    Execute a trade with balance validation and profit/loss tracking
    
    Required fields:
    - trade_type: 'buy', 'sell', or 'swap'
    - cryptocurrency: symbol (e.g., 'BTC')
    - amount: amount to trade
    - price: price per unit (optional for swap)
    - leverage: leverage amount (default: 1)
    
    For swap:
    - to_cryptocurrency: destination crypto symbol
    """
    try:
        trade_type = request.data.get('trade_type')
        cryptocurrency = request.data.get('cryptocurrency')
        amount = request.data.get('amount')
        price = request.data.get('price', 0)
        leverage = int(request.data.get('leverage', 1))
        
        if not all([trade_type, cryptocurrency, amount]):
            return Response(
                {'error': 'Missing required fields: trade_type, cryptocurrency, amount'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize biased trade executor
        executor = BiasedTradeExecutor(request.user)
        
        # Execute trade based on type
        if trade_type == 'buy':
            if not price or Decimal(price) <= 0:
                return Response(
                    {'error': 'Price must be greater than 0 for buy orders'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            trade, outcome = executor.execute_biased_buy_order(cryptocurrency, amount, price, leverage)
            
            # Include outcome info in response
            outcome_info = {
                'expected_outcome': outcome.outcome,
                'expected_percentage': float(outcome.outcome_percentage),
                'target_close_time': outcome.target_close_time.isoformat(),
                'duration_seconds': outcome.duration_seconds
            }
            
        elif trade_type == 'sell':
            if not price or Decimal(price) <= 0:
                return Response(
                    {'error': 'Price must be greater than 0 for sell orders'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            trade = executor.execute_biased_sell_order(cryptocurrency, amount, price, leverage)
            outcome_info = None  # Sell orders use predetermined outcome from buy
            
        elif trade_type == 'swap':
            to_cryptocurrency = request.data.get('to_cryptocurrency')
            if not to_cryptocurrency:
                return Response(
                    {'error': 'to_cryptocurrency is required for swap'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            trade = executor.execute_swap(cryptocurrency, to_cryptocurrency, amount)
            
        else:
            return Response(
                {'error': 'Invalid trade_type. Must be: buy, sell, or swap'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Serialize and return trade
        serializer = TradeSerializer(trade)
        response_data = {
            'success': True,
            'message': f'{trade_type.capitalize()} order executed successfully',
            'trade': serializer.data,
            'pnl': float(trade.pnl),
            'fees': float(trade.fees)
        }
        
        # Add outcome info for buy orders
        if trade_type == 'buy' and 'outcome_info' in locals():
            response_data['outcome'] = outcome_info
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except ValidationError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        # Log the full error for debugging
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'Trade execution failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_balance(request):
    """
    Check available balance for a specific cryptocurrency
    
    Query params:
    - symbol: cryptocurrency symbol (e.g., 'BTC', 'ETH', 'USDT')
    """
    try:
        symbol = request.query_params.get('symbol', 'USDT')
        
        executor = TradeExecutor(request.user)
        available_balance = executor.get_available_balance(symbol)
        
        # Also get USD value
        try:
            crypto = Cryptocurrency.objects.get(symbol=symbol)
            usd_value = available_balance * crypto.current_price
        except Cryptocurrency.DoesNotExist:
            usd_value = 0
        
        return Response({
            'symbol': symbol,
            'available_balance': float(available_balance),
            'usd_value': float(usd_value)
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_trading_history(request):
    """
    Get user's trading history with profit/loss summary
    
    Query params:
    - limit: number of trades to return (default: 50)
    - trade_type: filter by type (buy, sell, swap)
    """
    try:
        limit = int(request.query_params.get('limit', 50))
        trade_type = request.query_params.get('trade_type')
        
        # Get regular trades
        trades = Trade.objects.filter(
            user=request.user,
            status='executed'
        ).order_by('-executed_at')
        
        if trade_type:
            trades = trades.filter(trade_type=trade_type)
        
        # Get strategy executions and convert to trade-like format
        from strategy_engine.models import StrategyExecution
        strategy_executions = StrategyExecution.objects.filter(
            strategy__user=request.user,
            action__in=['buy', 'sell']  # Only include actual trades, not holds
        ).order_by('-execution_time')
        
        # Combine and sort all activities
        all_activities = []
        
        # Add regular trades
        for trade in trades:
            all_activities.append({
                'id': trade.id,
                'type': 'trade',
                'trade_type': trade.trade_type,
                'cryptocurrency': trade.cryptocurrency.symbol,
                'cryptocurrency_symbol': trade.cryptocurrency.symbol,
                'amount': float(trade.amount),
                'price': float(trade.price),
                'total_value': float(trade.total_value),
                'leverage': float(trade.leverage),
                'status': trade.status,
                'pnl': float(trade.pnl),
                'profit_loss': float(trade.pnl),
                'fees': float(trade.fees),
                'created_at': trade.created_at.isoformat(),
                'executed_at': trade.executed_at.isoformat() if trade.executed_at else trade.created_at.isoformat(),
            })
        
        # Add strategy executions
        for execution in strategy_executions:
            all_activities.append({
                'id': f"strategy_{execution.id}",
                'type': 'strategy',
                'trade_type': execution.action,
                'cryptocurrency': execution.symbol,
                'cryptocurrency_symbol': execution.symbol,
                'amount': float(execution.quantity) if execution.quantity else 0,
                'price': float(execution.price) if execution.price else 0,
                'total_value': float(execution.quantity * execution.price) if execution.quantity and execution.price else 0,
                'leverage': 1.0,  # Strategies typically don't use leverage
                'status': 'executed',
                'pnl': float(execution.pnl) if execution.pnl else 0,
                'profit_loss': float(execution.pnl) if execution.pnl else 0,
                'fees': 0.0,  # Strategy executions don't have separate fees
                'created_at': execution.execution_time.isoformat(),
                'executed_at': execution.execution_time.isoformat(),
                'strategy_name': execution.strategy.name,
                'reason': execution.reason,
            })
        
        # Sort by execution time (newest first) and limit
        all_activities.sort(key=lambda x: x['executed_at'], reverse=True)
        all_activities = all_activities[:limit]
        
        # Calculate total PnL from both trades and strategy executions
        executor = TradeExecutor(request.user)
        total_pnl = executor.calculate_total_pnl()
        
        # Add strategy execution PnL to total
        strategy_pnl = sum(float(exec.pnl) for exec in strategy_executions if exec.pnl)
        total_pnl += strategy_pnl
        
        # Count by type
        buy_count = len([a for a in all_activities if a['trade_type'] == 'buy'])
        sell_count = len([a for a in all_activities if a['trade_type'] == 'sell'])
        strategy_count = len([a for a in all_activities if a['type'] == 'strategy'])
        
        return Response({
            'results': all_activities,  # Changed from 'trades' to 'results' to match frontend expectation
            'total_count': len(all_activities),
            'total_pnl': float(total_pnl),
            'summary': {
                'total_trades': len(all_activities),
                'buy_trades': buy_count,
                'sell_trades': sell_count,
                'strategy_executions': strategy_count,
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class DeductBalanceView(APIView):
    """
    Deduct balance from user wallet for strategy trades and ongoing trades.
    This ensures the user's balance is reduced when creating trades.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            amount = Decimal(str(request.data.get('amount', 0)))
            cryptocurrency_symbol = request.data.get('cryptocurrency_symbol', 'BTC')
            trade_type = request.data.get('trade_type', 'strategy')
            leverage = int(request.data.get('leverage', 1))
            description = request.data.get('description', 'Trade deduction')
            trade_amount = Decimal(str(request.data.get('trade_amount', 0)))
            entry_price = Decimal(str(request.data.get('entry_price', 0)))

            if amount <= 0:
                return Response(
                    {'error': 'Amount must be greater than zero'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get or create multi-currency wallet
            import uuid
            wallet, created = MultiCurrencyWallet.objects.get_or_create(
                user=request.user,
                defaults={
                    'wallet_address': f'MCW_{uuid.uuid4().hex[:16].upper()}',
                    'is_active': True
                }
            )

            # Get USDT balance (assuming deductions are in USDT)
            try:
                usdt = Cryptocurrency.objects.get(symbol='USDT')
                usdt_balance, _ = CryptoBalance.objects.get_or_create(
                    wallet=wallet,
                    cryptocurrency=usdt,
                    defaults={'balance': Decimal('0')}
                )
            except Cryptocurrency.DoesNotExist:
                return Response(
                    {'error': 'USDT not configured in system'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if user has sufficient balance
            if usdt_balance.available_balance < amount:
                return Response(
                    {'error': f'Insufficient balance. Required: {amount} USDT, Available: {usdt_balance.available_balance} USDT'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with db_transaction.atomic():
                # DON'T deduct from balance - strategy trades are simulated only
                # usdt_balance.balance -= amount  # DISABLED - no actual balance deduction
                # usdt_balance.save()  # DISABLED

                # Get or create the cryptocurrency
                try:
                    cryptocurrency = Cryptocurrency.objects.get(symbol=cryptocurrency_symbol)
                except Cryptocurrency.DoesNotExist:
                    cryptocurrency = None

                # Create a trade record
                trade = Trade.objects.create(
                    user=request.user,
                    cryptocurrency=cryptocurrency,
                    trade_type=trade_type,
                    amount=trade_amount if trade_amount > 0 else Decimal('0'),
                    trade_sum=trade_amount if trade_amount > 0 else Decimal('0'),
                    price=entry_price if entry_price > 0 else Decimal('0'),
                    entry_price=entry_price if entry_price > 0 else Decimal('0'),
                    total_value=amount,
                    leverage=leverage,
                    status='pending',
                    pnl=-amount,  # Negative PnL (cost of trade)
                    fees=Decimal('0'),
                    is_strategy_trade=True
                )

                return Response({
                    'success': True,
                    'message': f'Successfully deducted {amount} USDT from balance',
                    'trade_id': trade.id,
                    'remaining_balance': usdt_balance.available_balance,
                    'deducted_amount': amount
                }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {'error': f'Invalid amount format: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StopTradeView(APIView):
    """
    Stop a trade and return the remaining trade_sum to user's balance.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, trade_id):
        try:
            trade = Trade.objects.get(id=trade_id, user=request.user)
            
            if trade.trade_sum <= 0:
                return Response(
                    {'error': 'Trade already completed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with db_transaction.atomic():
                # Calculate amount to return (proportional to remaining trade_sum)
                initial_deduction = float(trade.total_value)
                remaining_percentage = float(trade.trade_sum) / float(trade.amount) if float(trade.amount) > 0 else 0
                amount_to_return = Decimal(str(initial_deduction * remaining_percentage))
                
                # Get user wallet
                wallet = MultiCurrencyWallet.objects.get(user=request.user)
                
                # Get USDT balance
                usdt = Cryptocurrency.objects.get(symbol='USDT')
                usdt_balance, _ = CryptoBalance.objects.get_or_create(
                    wallet=wallet,
                    cryptocurrency=usdt,
                    defaults={'balance': Decimal('0')}
                )
                
                # DON'T return balance - no deduction was made
                old_balance = usdt_balance.balance
                # usdt_balance.balance += amount_to_return  # DISABLED - no balance return
                # usdt_balance.save()  # DISABLED
                
                # Update trade status
                trade.status = 'cancelled'
                trade.save()
                
                # Send balance update via WebSocket
                from channels.layers import get_channel_layer
                from asgiref.sync import async_to_sync
                
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'trades_user_{request.user.id}',
                    {
                        'type': 'balance_update',
                        'balance': str(usdt_balance.balance),
                        'currency': 'USDT',
                        'reason': 'trade_stopped',
                        'amount_returned': str(amount_to_return),
                        'timestamp': timezone.now().isoformat()
                    }
                )
                
                return Response({
                    'success': True,
                    'message': f'Trade stopped. {amount_to_return} USDT returned to balance',
                    'amount_returned': str(amount_to_return),
                    'old_balance': str(old_balance),
                    'new_balance': str(usdt_balance.balance),
                    'trade_id': trade.id
                }, status=status.HTTP_200_OK)
                
        except Trade.DoesNotExist:
            return Response(
                {'error': 'Trade not found or you do not have permission'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
