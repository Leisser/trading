from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Avg, Q
from django.utils import timezone
from decimal import Decimal
import requests
from datetime import datetime, timedelta

from .models import (
    CryptoIndex, IndexComponent, CryptoInvestment, 
    InvestmentTransaction, IndexPriceHistory, Cryptocurrency
)
from .serializers import (
    CryptoIndexSerializer, CryptoIndexListSerializer, CryptoInvestmentSerializer,
    CryptoInvestmentListSerializer, InvestmentCreateSerializer, 
    TransactionCreateSerializer, InvestmentTransactionSerializer,
    IndexPriceHistorySerializer, InvestmentPerformanceSerializer,
    PortfolioAllocationSerializer
)


class CryptoIndexListView(generics.ListAPIView):
    """List all available crypto indices"""
    queryset = CryptoIndex.objects.filter(is_active=True, is_tradeable=True)
    serializer_class = CryptoIndexListSerializer
    permission_classes = [IsAuthenticated]


class CryptoIndexDetailView(generics.RetrieveAPIView):
    """Get detailed information about a specific crypto index"""
    queryset = CryptoIndex.objects.filter(is_active=True)
    serializer_class = CryptoIndexSerializer
    permission_classes = [IsAuthenticated]


class CryptoInvestmentListView(generics.ListCreateAPIView):
    """List user's crypto investments and create new ones"""
    serializer_class = CryptoInvestmentListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CryptoInvestment.objects.filter(
            user=self.request.user
        ).select_related('crypto_index', 'cryptocurrency')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InvestmentCreateSerializer
        return CryptoInvestmentListSerializer
    
    def perform_create(self, serializer):
        # Get current Bitcoin price for USD conversion
        btc_price = self.get_btc_price()
        
        investment = serializer.save(user=self.request.user)
        initial_investment_btc = serializer.validated_data['initial_investment_btc']
        
        # Set initial values
        investment.total_invested_btc = initial_investment_btc
        investment.total_invested_usd = initial_investment_btc * btc_price
        investment.current_value_btc = initial_investment_btc
        investment.current_value_usd = initial_investment_btc * btc_price
        
        # Set crypto_index or cryptocurrency based on investment type
        if serializer.validated_data.get('crypto_index_id'):
            investment.crypto_index_id = serializer.validated_data['crypto_index_id']
        elif serializer.validated_data.get('cryptocurrency_id'):
            investment.cryptocurrency_id = serializer.validated_data['cryptocurrency_id']
        
        investment.save()
        
        # Create initial investment transaction
        InvestmentTransaction.objects.create(
            investment=investment,
            transaction_type='deposit',
            amount_btc=initial_investment_btc,
            amount_usd=initial_investment_btc * btc_price,
            btc_price_at_transaction=btc_price,
            index_value_at_transaction=investment.crypto_index.current_value if investment.crypto_index else None,
            notes='Initial investment'
        )
    
    def get_btc_price(self):
        """Get current Bitcoin price from external API"""
        try:
            # Try to get from local cryptocurrency model first
            btc = Cryptocurrency.objects.filter(symbol='BTC').first()
            if btc and btc.current_price > 0:
                return btc.current_price
            
            # Fallback to external API
            response = requests.get(
                'https://api.coingecko.com/api/v3/simple/price',
                params={'ids': 'bitcoin', 'vs_currencies': 'usd'},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return Decimal(str(data['bitcoin']['usd']))
        except Exception as e:
            print(f"Error fetching Bitcoin price: {e}")
        
        # Default fallback price
        return Decimal('45000.00')


class CryptoInvestmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific crypto investment"""
    serializer_class = CryptoInvestmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CryptoInvestment.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        # Close the investment instead of deleting
        instance.status = 'closed'
        instance.closed_at = timezone.now()
        instance.save()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_investment_funds(request, investment_id):
    """Add funds to an existing investment"""
    investment = get_object_or_404(
        CryptoInvestment, 
        id=investment_id, 
        user=request.user
    )
    
    serializer = TransactionCreateSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['transaction_type'] != 'deposit':
            return Response(
                {'error': 'Transaction type must be deposit for adding funds'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        amount_btc = serializer.validated_data['amount_btc']
        btc_price = get_btc_price()
        
        # Create transaction
        transaction = InvestmentTransaction.objects.create(
            investment=investment,
            transaction_type='deposit',
            amount_btc=amount_btc,
            amount_usd=amount_btc * btc_price,
            btc_price_at_transaction=btc_price,
            index_value_at_transaction=investment.crypto_index.current_value if investment.crypto_index else None,
            notes=serializer.validated_data.get('notes', '')
        )
        
        # Update investment totals
        investment.total_invested_btc += amount_btc
        investment.total_invested_usd += amount_btc * btc_price
        investment.current_value_btc += amount_btc
        investment.current_value_usd += amount_btc * btc_price
        investment.save()
        
        return Response({
            'success': True,
            'message': 'Funds added successfully',
            'transaction': InvestmentTransactionSerializer(transaction).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw_investment_funds(request, investment_id):
    """Withdraw funds from an existing investment"""
    investment = get_object_or_404(
        CryptoInvestment, 
        id=investment_id, 
        user=request.user
    )
    
    serializer = TransactionCreateSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['transaction_type'] != 'withdraw':
            return Response(
                {'error': 'Transaction type must be withdraw for withdrawing funds'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        amount_btc = serializer.validated_data['amount_btc']
        
        if amount_btc > investment.current_value_btc:
            return Response(
                {'error': 'Withdrawal amount exceeds current investment value'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        btc_price = get_btc_price()
        
        # Create transaction
        transaction = InvestmentTransaction.objects.create(
            investment=investment,
            transaction_type='withdraw',
            amount_btc=amount_btc,
            amount_usd=amount_btc * btc_price,
            btc_price_at_transaction=btc_price,
            index_value_at_transaction=investment.crypto_index.current_value if investment.crypto_index else None,
            notes=serializer.validated_data.get('notes', '')
        )
        
        # Update investment totals
        investment.current_value_btc -= amount_btc
        investment.current_value_usd -= amount_btc * btc_price
        
        # Recalculate P&L
        investment.unrealized_pnl_btc = investment.current_value_btc - investment.total_invested_btc
        investment.unrealized_pnl_usd = investment.current_value_usd - investment.total_invested_usd
        investment.unrealized_pnl_percent = (
            (investment.unrealized_pnl_btc / investment.total_invested_btc) * 100
            if investment.total_invested_btc > 0 else 0
        )
        
        investment.save()
        
        return Response({
            'success': True,
            'message': 'Funds withdrawn successfully',
            'transaction': InvestmentTransactionSerializer(transaction).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investment_performance(request, investment_id):
    """Get detailed performance analytics for an investment"""
    investment = get_object_or_404(
        CryptoInvestment, 
        id=investment_id, 
        user=request.user
    )
    
    # Calculate performance metrics
    duration = (timezone.now() - investment.started_at).days
    total_return = investment.current_value_btc - investment.total_invested_btc
    total_return_percent = (
        (total_return / investment.total_invested_btc) * 100
        if investment.total_invested_btc > 0 else 0
    )
    
    # Calculate average daily return
    average_daily_return = (
        total_return_percent / duration if duration > 0 else 0
    )
    
    performance_data = {
        'total_invested': investment.total_invested_btc,
        'current_value': investment.current_value_btc,
        'total_return': total_return,
        'total_return_percent': total_return_percent,
        'unrealized_pnl': investment.unrealized_pnl_btc,
        'all_time_high': investment.all_time_high_value,
        'max_drawdown': investment.max_drawdown_percent,
        'investment_duration_days': duration,
        'average_daily_return': average_daily_return / 100,  # Convert to decimal
        'sharpe_ratio': None,  # Would need more sophisticated calculation
        'volatility': None,  # Would need historical price data
    }
    
    serializer = InvestmentPerformanceSerializer(performance_data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def portfolio_allocation(request):
    """Get user's portfolio allocation breakdown"""
    investments = CryptoInvestment.objects.filter(
        user=request.user,
        status='active'
    ).select_related('crypto_index', 'cryptocurrency')
    
    total_portfolio_value = sum(inv.current_value_btc for inv in investments)
    
    allocation_data = []
    for investment in investments:
        allocation_percentage = (
            (investment.current_value_btc / total_portfolio_value) * 100
            if total_portfolio_value > 0 else 0
        )
        
        allocation_data.append({
            'investment_name': investment.name,
            'investment_type': investment.investment_type,
            'target_name': investment.investment_target_name,
            'current_value_btc': investment.current_value_btc,
            'allocation_percentage': allocation_percentage,
            'performance_percent': investment.total_return_percent,
            'is_profitable': investment.is_profitable
        })
    
    serializer = PortfolioAllocationSerializer(allocation_data, many=True)
    return Response({
        'total_portfolio_value_btc': total_portfolio_value,
        'allocations': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investment_history(request, investment_id):
    """Get transaction history for a specific investment"""
    investment = get_object_or_404(
        CryptoInvestment, 
        id=investment_id, 
        user=request.user
    )
    
    transactions = investment.transactions.all()
    serializer = InvestmentTransactionSerializer(transactions, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index_price_history(request, index_id):
    """Get price history for a crypto index"""
    crypto_index = get_object_or_404(CryptoIndex, id=index_id)
    
    # Get date range from query parameters
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    price_history = IndexPriceHistory.objects.filter(
        crypto_index=crypto_index,
        timestamp__gte=start_date
    ).order_by('timestamp')
    
    serializer = IndexPriceHistorySerializer(price_history, many=True)
    return Response(serializer.data)


def get_btc_price():
    """Helper function to get current Bitcoin price"""
    try:
        # Try to get from local cryptocurrency model first
        btc = Cryptocurrency.objects.filter(symbol='BTC').first()
        if btc and btc.current_price > 0:
            return btc.current_price
        
        # Fallback to external API
        response = requests.get(
            'https://api.coingecko.com/api/v3/simple/price',
            params={'ids': 'bitcoin', 'vs_currencies': 'usd'},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return Decimal(str(data['bitcoin']['usd']))
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
    
    # Default fallback price
    return Decimal('45000.00')


# Background task functions (would be called by Celery or similar)
def update_investment_values():
    """Update current values for all active investments"""
    btc_price = get_btc_price()
    
    for investment in CryptoInvestment.objects.filter(status='active'):
        if investment.crypto_index:
            # For index investments, use index performance
            # This would need more sophisticated calculation based on index components
            pass
        elif investment.cryptocurrency:
            # For single crypto investments, use current price
            crypto_price = investment.cryptocurrency.current_price
            if crypto_price > 0:
                # Calculate new value based on price change
                price_change_percent = (
                    (crypto_price - investment.cryptocurrency.current_price) / 
                    investment.cryptocurrency.current_price
                ) if investment.cryptocurrency.current_price > 0 else 0
                
                investment.current_value_btc *= (1 + price_change_percent)
                investment.current_value_usd = investment.current_value_btc * btc_price
                
                # Update P&L
                investment.unrealized_pnl_btc = investment.current_value_btc - investment.total_invested_btc
                investment.unrealized_pnl_usd = investment.current_value_usd - investment.total_invested_usd
                investment.unrealized_pnl_percent = (
                    (investment.unrealized_pnl_btc / investment.total_invested_btc) * 100
                    if investment.total_invested_btc > 0 else 0
                )
                
                # Update all-time high and max drawdown
                if investment.current_value_btc > investment.all_time_high_value:
                    investment.all_time_high_value = investment.current_value_btc
                
                if investment.all_time_high_value > 0:
                    drawdown = ((investment.all_time_high_value - investment.current_value_btc) / 
                               investment.all_time_high_value) * 100
                    if drawdown > investment.max_drawdown_percent:
                        investment.max_drawdown_percent = drawdown
                
                investment.save()