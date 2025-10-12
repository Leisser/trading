"""
Investment Management API Views
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum, Avg, Count, Q
from datetime import datetime, timedelta

from .models import Investment, InvestmentTransaction
from .serializers import (
    InvestmentSerializer, InvestmentTransactionSerializer, CreateInvestmentSerializer,
    InvestmentPerformanceSerializer, CryptoIndexSerializer, CryptocurrencySerializer
)
from trades.models import CryptoIndex, Cryptocurrency
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class InvestmentListView(generics.ListCreateAPIView):
    """List and create investments"""
    serializer_class = InvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Investment.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateInvestmentSerializer
        return InvestmentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvestmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Manage individual investments"""
    serializer_class = InvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Investment.objects.filter(user=self.request.user)


class InvestmentTransactionListView(generics.ListCreateAPIView):
    """List and create investment transactions"""
    serializer_class = InvestmentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        investment_id = self.kwargs.get('investment_id')
        return InvestmentTransaction.objects.filter(
            investment__id=investment_id,
            investment__user=self.request.user
        )
    
    def perform_create(self, serializer):
        investment_id = self.kwargs.get('investment_id')
        investment = Investment.objects.get(id=investment_id, user=self.request.user)
        serializer.save(investment=investment)


class CryptoIndexListView(generics.ListAPIView):
    """List available crypto indices"""
    serializer_class = CryptoIndexSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CryptoIndex.objects.filter(is_active=True, is_tradeable=True)


class CryptocurrencyListView(generics.ListAPIView):
    """List available cryptocurrencies"""
    serializer_class = CryptocurrencySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cryptocurrency.objects.filter(is_active=True, is_tradeable=True)
    filter_backends = []  # Disable filters to avoid JSONField issues


class InvestmentPerformanceView(APIView):
    """Get investment performance analytics"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'investment_id',
                openapi.IN_QUERY,
                description="Specific investment ID",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'period',
                openapi.IN_QUERY,
                description="Time period for analysis",
                type=openapi.TYPE_STRING,
                enum=['7d', '30d', '90d', '1y', 'all'],
                default='30d'
            )
        ]
    )
    def get(self, request):
        investment_id = request.query_params.get('investment_id')
        period = request.query_params.get('period', '30d')
        
        try:
            if investment_id:
                investments = Investment.objects.filter(
                    id=investment_id, 
                    user=request.user
                )
            else:
                investments = Investment.objects.filter(user=request.user)
            
            if not investments.exists():
                return Response(
                    {'error': 'No investments found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Calculate performance metrics
            performance_data = []
            total_invested = Decimal('0')
            total_current_value = Decimal('0')
            total_pnl = Decimal('0')
            
            for investment in investments:
                total_invested += investment.total_invested_usd
                total_current_value += investment.current_value_usd
                total_pnl += investment.unrealized_pnl_usd
                
                performance_data.append({
                    'investment_id': investment.id,
                    'name': investment.name,
                    'investment_type': investment.investment_type,
                    'total_invested_usd': investment.total_invested_usd,
                    'current_value_usd': investment.current_value_usd,
                    'unrealized_pnl_usd': investment.unrealized_pnl_usd,
                    'unrealized_pnl_percent': investment.unrealized_pnl_percent,
                    'total_return_percent': investment.total_return_percent,
                    'is_profitable': investment.is_profitable,
                    'started_at': investment.started_at,
                    'last_updated': investment.last_updated
                })
            
            # Calculate overall portfolio performance
            overall_return_percent = 0
            if total_invested > 0:
                overall_return_percent = ((total_current_value - total_invested) / total_invested) * 100
            
            return Response({
                'investments': performance_data,
                'portfolio_summary': {
                    'total_investments': len(performance_data),
                    'total_invested_usd': total_invested,
                    'total_current_value_usd': total_current_value,
                    'total_pnl_usd': total_pnl,
                    'overall_return_percent': overall_return_percent,
                    'profitable_investments': len([inv for inv in performance_data if inv['is_profitable']])
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def invest_in_index(request, index_id):
    """Invest in a crypto index"""
    try:
        index = CryptoIndex.objects.get(id=index_id, is_active=True, is_tradeable=True)
        
        amount_btc = Decimal(request.data.get('amount_btc', 0))
        amount_usd = Decimal(request.data.get('amount_usd', 0))
        
        if amount_btc <= 0 and amount_usd <= 0:
            return Response(
                {'error': 'Amount must be greater than 0'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create investment
        investment = Investment.objects.create(
            user=request.user,
            investment_type='index',
            crypto_index=index,
            name=f"{index.name} Investment",
            total_invested_btc=amount_btc,
            total_invested_usd=amount_usd,
            current_value_btc=amount_btc,
            current_value_usd=amount_usd,
            status='active'
        )
        
        # Create initial transaction
        InvestmentTransaction.objects.create(
            investment=investment,
            transaction_type='deposit',
            amount_btc=amount_btc,
            amount_usd=amount_usd,
            btc_price_at_transaction=amount_usd / amount_btc if amount_btc > 0 else 0,
            index_value_at_transaction=index.current_value,
            notes='Initial investment'
        )
        
        serializer = InvestmentSerializer(investment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except CryptoIndex.DoesNotExist:
        return Response(
            {'error': 'Index not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def invest_in_crypto(request, crypto_id):
    """Invest in a single cryptocurrency"""
    try:
        crypto = Cryptocurrency.objects.get(id=crypto_id, is_active=True, is_tradeable=True)
        
        amount_btc = Decimal(request.data.get('amount_btc', 0))
        amount_usd = Decimal(request.data.get('amount_usd', 0))
        
        if amount_btc <= 0 and amount_usd <= 0:
            return Response(
                {'error': 'Amount must be greater than 0'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create investment
        investment = Investment.objects.create(
            user=request.user,
            investment_type='single_crypto',
            cryptocurrency=crypto,
            name=f"{crypto.name} Investment",
            total_invested_btc=amount_btc,
            total_invested_usd=amount_usd,
            current_value_btc=amount_btc,
            current_value_usd=amount_usd,
            status='active'
        )
        
        # Create initial transaction
        InvestmentTransaction.objects.create(
            investment=investment,
            transaction_type='deposit',
            amount_btc=amount_btc,
            amount_usd=amount_usd,
            btc_price_at_transaction=amount_usd / amount_btc if amount_btc > 0 else 0,
            notes='Initial investment'
        )
        
        serializer = InvestmentSerializer(investment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Cryptocurrency.DoesNotExist:
        return Response(
            {'error': 'Cryptocurrency not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def setup_dca(request, investment_id):
    """Setup Dollar Cost Averaging for an investment"""
    try:
        investment = Investment.objects.get(id=investment_id, user=request.user)
        
        dca_amount_btc = Decimal(request.data.get('dca_amount_btc', 0))
        dca_frequency = request.data.get('dca_frequency', 'monthly')
        
        if dca_amount_btc <= 0:
            return Response(
                {'error': 'DCA amount must be greater than 0'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update investment with DCA settings
        investment.investment_type = 'dca'
        investment.dca_amount_btc = dca_amount_btc
        investment.dca_frequency = dca_frequency
        
        # Calculate next DCA date
        if dca_frequency == 'daily':
            investment.next_dca_date = timezone.now() + timedelta(days=1)
        elif dca_frequency == 'weekly':
            investment.next_dca_date = timezone.now() + timedelta(weeks=1)
        elif dca_frequency == 'monthly':
            investment.next_dca_date = timezone.now() + timedelta(days=30)
        
        investment.save()
        
        serializer = InvestmentSerializer(investment)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Investment.DoesNotExist:
        return Response(
            {'error': 'Investment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_auto_compound(request, investment_id):
    """Toggle auto-compound feature for an investment"""
    try:
        investment = Investment.objects.get(id=investment_id, user=request.user)
        investment.auto_compound = not investment.auto_compound
        investment.save()
        
        serializer = InvestmentSerializer(investment)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Investment.DoesNotExist:
        return Response(
            {'error': 'Investment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
