"""
Portfolio Management API Views for balance tracking, P&L, and analytics.
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum, Avg, Count, Q
from datetime import datetime, timedelta
import json

from .models import Portfolio, PortfolioBalance, Transaction, PnLRecord, AssetAllocation
from .services import PortfolioService, PnLService, RiskAnalyticsService
from .serializers import (
    PortfolioSerializer, PortfolioBalanceSerializer, TransactionSerializer,
    PnLRecordSerializer, AssetAllocationSerializer, PortfolioSummarySerializer,
    PerformanceAnalyticsSerializer, RiskMetricsSerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PortfolioListView(generics.ListCreateAPIView):
    """List and create portfolios"""
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PortfolioDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Manage individual portfolios"""
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

class PortfolioSummaryView(APIView):
    """Get comprehensive portfolio summary"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'portfolio_id',
                openapi.IN_QUERY,
                description="Portfolio ID (optional, defaults to primary portfolio)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'currency',
                openapi.IN_QUERY,
                description="Base currency for calculations",
                type=openapi.TYPE_STRING,
                default='USD'
            )
        ]
    )
    def get(self, request):
        portfolio_id = request.query_params.get('portfolio_id')
        currency = request.query_params.get('currency', 'USD')
        
        try:
            if portfolio_id:
                portfolio = Portfolio.objects.get(id=portfolio_id, user=request.user)
            else:
                portfolio = Portfolio.objects.filter(user=request.user).first()
            
            if not portfolio:
                return Response(
                    {'error': 'No portfolio found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get portfolio summary
            summary = PortfolioService.get_portfolio_summary(portfolio, currency)
            serializer = PortfolioSummarySerializer(summary)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Portfolio.DoesNotExist:
            return Response(
                {'error': 'Portfolio not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class PortfolioBalanceView(APIView):
    """Get portfolio balances"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'portfolio_id',
                openapi.IN_QUERY,
                description="Portfolio ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'asset',
                openapi.IN_QUERY,
                description="Filter by specific asset",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request):
        portfolio_id = request.query_params.get('portfolio_id')
        asset = request.query_params.get('asset')
        
        try:
            if portfolio_id:
                portfolio = Portfolio.objects.get(id=portfolio_id, user=request.user)
            else:
                portfolio = Portfolio.objects.filter(user=request.user).first()
            
            if not portfolio:
                return Response(
                    {'error': 'No portfolio found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            balances = PortfolioService.get_portfolio_balances(portfolio, asset)
            serializer = PortfolioBalanceSerializer(balances, many=True)
            
            return Response({
                'balances': serializer.data,
                'total_assets': len(balances)
            }, status=status.HTTP_200_OK)
            
        except Portfolio.DoesNotExist:
            return Response(
                {'error': 'Portfolio not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class TransactionListView(generics.ListCreateAPIView):
    """List and create transactions"""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(portfolio__user=self.request.user).order_by('-timestamp')
    
    def perform_create(self, serializer):
        # Get user's primary portfolio
        portfolio = Portfolio.objects.filter(user=self.request.user).first()
        if not portfolio:
            portfolio = Portfolio.objects.create(
                user=self.request.user,
                name="Primary Portfolio"
            )
        serializer.save(portfolio=portfolio)

class PnLAnalyticsView(APIView):
    """Get P&L analytics and performance metrics"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'portfolio_id',
                openapi.IN_QUERY,
                description="Portfolio ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'period',
                openapi.IN_QUERY,
                description="Time period for analysis",
                type=openapi.TYPE_STRING,
                enum=['1d', '7d', '30d', '90d', '1y', 'all'],
                default='30d'
            ),
            openapi.Parameter(
                'currency',
                openapi.IN_QUERY,
                description="Base currency",
                type=openapi.TYPE_STRING,
                default='USD'
            )
        ]
    )
    def get(self, request):
        portfolio_id = request.query_params.get('portfolio_id')
        period = request.query_params.get('period', '30d')
        currency = request.query_params.get('currency', 'USD')
        
        try:
            if portfolio_id:
                portfolio = Portfolio.objects.get(id=portfolio_id, user=request.user)
            else:
                portfolio = Portfolio.objects.filter(user=request.user).first()
            
            if not portfolio:
                return Response(
                    {'error': 'No portfolio found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get P&L analytics
            analytics = PnLService.get_pnl_analytics(portfolio, period, currency)
            serializer = PerformanceAnalyticsSerializer(analytics)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Portfolio.DoesNotExist:
            return Response(
                {'error': 'Portfolio not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class AssetAllocationView(APIView):
    """Get asset allocation breakdown"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'portfolio_id',
                openapi.IN_QUERY,
                description="Portfolio ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'currency',
                openapi.IN_QUERY,
                description="Base currency",
                type=openapi.TYPE_STRING,
                default='USD'
            )
        ]
    )
    def get(self, request):
        portfolio_id = request.query_params.get('portfolio_id')
        currency = request.query_params.get('currency', 'USD')
        
        try:
            if portfolio_id:
                portfolio = Portfolio.objects.get(id=portfolio_id, user=request.user)
            else:
                portfolio = Portfolio.objects.filter(user=request.user).first()
            
            if not portfolio:
                return Response(
                    {'error': 'No portfolio found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get asset allocation
            allocation = PortfolioService.get_asset_allocation(portfolio, currency)
            serializer = AssetAllocationSerializer(allocation, many=True)
            
            return Response({
                'allocation': serializer.data,
                'total_value': sum(item['value'] for item in allocation)
            }, status=status.HTTP_200_OK)
            
        except Portfolio.DoesNotExist:
            return Response(
                {'error': 'Portfolio not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class RiskMetricsView(APIView):
    """Get risk metrics and analytics"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'portfolio_id',
                openapi.IN_QUERY,
                description="Portfolio ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'period',
                openapi.IN_QUERY,
                description="Time period for risk analysis",
                type=openapi.TYPE_STRING,
                enum=['7d', '30d', '90d', '1y'],
                default='30d'
            )
        ]
    )
    def get(self, request):
        portfolio_id = request.query_params.get('portfolio_id')
        period = request.query_params.get('period', '30d')
        
        try:
            if portfolio_id:
                portfolio = Portfolio.objects.get(id=portfolio_id, user=request.user)
            else:
                portfolio = Portfolio.objects.filter(user=request.user).first()
            
            if not portfolio:
                return Response(
                    {'error': 'No portfolio found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get risk metrics
            risk_metrics = RiskAnalyticsService.get_risk_metrics(portfolio, period)
            serializer = RiskMetricsSerializer(risk_metrics)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Portfolio.DoesNotExist:
            return Response(
                {'error': 'Portfolio not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class PerformanceComparisonView(APIView):
    """Compare portfolio performance against benchmarks"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'portfolio_id',
                openapi.IN_QUERY,
                description="Portfolio ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'benchmark',
                openapi.IN_QUERY,
                description="Benchmark to compare against",
                type=openapi.TYPE_STRING,
                enum=['BTC', 'ETH', 'SP500', 'NASDAQ'],
                default='BTC'
            ),
            openapi.Parameter(
                'period',
                openapi.IN_QUERY,
                description="Time period for comparison",
                type=openapi.TYPE_STRING,
                enum=['7d', '30d', '90d', '1y'],
                default='30d'
            )
        ]
    )
    def get(self, request):
        portfolio_id = request.query_params.get('portfolio_id')
        benchmark = request.query_params.get('benchmark', 'BTC')
        period = request.query_params.get('period', '30d')
        
        try:
            if portfolio_id:
                portfolio = Portfolio.objects.get(id=portfolio_id, user=request.user)
            else:
                portfolio = Portfolio.objects.filter(user=request.user).first()
            
            if not portfolio:
                return Response(
                    {'error': 'No portfolio found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get performance comparison
            comparison = PnLService.get_performance_comparison(portfolio, benchmark, period)
            
            return Response(comparison, status=status.HTTP_200_OK)
            
        except Portfolio.DoesNotExist:
            return Response(
                {'error': 'Portfolio not found'},
                status=status.HTTP_404_NOT_FOUND
            )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def rebalance_portfolio(request):
    """Rebalance portfolio to target allocation"""
    portfolio_id = request.data.get('portfolio_id')
    target_allocation = request.data.get('target_allocation', {})
    
    try:
        if portfolio_id:
            portfolio = Portfolio.objects.get(id=portfolio_id, user=request.user)
        else:
            portfolio = Portfolio.objects.filter(user=request.user).first()
        
        if not portfolio:
            return Response(
                {'error': 'No portfolio found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Execute rebalancing
        result = PortfolioService.rebalance_portfolio(portfolio, target_allocation)
        
        return Response({
            'message': 'Portfolio rebalancing initiated',
            'result': result
        }, status=status.HTTP_200_OK)
        
    except Portfolio.DoesNotExist:
        return Response(
            {'error': 'Portfolio not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def portfolio_history(request):
    """Get portfolio value history"""
    portfolio_id = request.query_params.get('portfolio_id')
    period = request.query_params.get('period', '30d')
    
    try:
        if portfolio_id:
            portfolio = Portfolio.objects.get(id=portfolio_id, user=request.user)
        else:
            portfolio = Portfolio.objects.filter(user=request.user).first()
        
        if not portfolio:
            return Response(
                {'error': 'No portfolio found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get portfolio history
        history = PortfolioService.get_portfolio_history(portfolio, period)
        
        return Response({
            'history': history,
            'period': period
        }, status=status.HTTP_200_OK)
        
    except Portfolio.DoesNotExist:
        return Response(
            {'error': 'Portfolio not found'},
            status=status.HTTP_404_NOT_FOUND
        )
