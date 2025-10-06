"""
Views for trades app - Cryptocurrency management and trading operations.
"""
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Sum
from django_filters.rest_framework import DjangoFilterBackend
from decimal import Decimal
import json

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
    - category: Filter by category
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
    filterset_fields = ['is_featured', 'is_stablecoin', 'is_active', 'categories']
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
