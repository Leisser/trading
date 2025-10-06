"""
Strategy Engine API Views
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Sum, Avg, Count, Q
from datetime import datetime, timedelta, date
from decimal import Decimal

from .models import TradingStrategy, StrategyExecution, StrategyPerformance, StrategyAlert
from .serializers import (
    TradingStrategySerializer, CreateTradingStrategySerializer, StrategyExecutionSerializer,
    StrategyPerformanceSerializer, StrategyAlertSerializer, ExecuteStrategySerializer,
    StrategyAnalyticsSerializer, StrategyBacktestSerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TradingStrategyListView(generics.ListCreateAPIView):
    """List and create trading strategies"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TradingStrategy.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTradingStrategySerializer
        return TradingStrategySerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TradingStrategyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Manage individual trading strategies"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TradingStrategySerializer
    
    def get_queryset(self):
        return TradingStrategy.objects.filter(user=self.request.user)


class StrategyExecutionListView(generics.ListAPIView):
    """List strategy executions"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StrategyExecutionSerializer
    
    def get_queryset(self):
        strategy_id = self.kwargs.get('strategy_id')
        return StrategyExecution.objects.filter(
            strategy__id=strategy_id,
            strategy__user=self.request.user
        )


class StrategyPerformanceListView(generics.ListAPIView):
    """List strategy performance records"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StrategyPerformanceSerializer
    
    def get_queryset(self):
        strategy_id = self.kwargs.get('strategy_id')
        return StrategyPerformance.objects.filter(
            strategy__id=strategy_id,
            strategy__user=self.request.user
        )


class StrategyAlertListView(generics.ListAPIView):
    """List strategy alerts"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StrategyAlertSerializer
    
    def get_queryset(self):
        strategy_id = self.kwargs.get('strategy_id')
        return StrategyAlert.objects.filter(
            strategy__id=strategy_id,
            strategy__user=self.request.user
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def start_strategy(request, strategy_id):
    """Start a trading strategy"""
    try:
        strategy = TradingStrategy.objects.get(id=strategy_id, user=request.user)
        
        if strategy.is_active:
            return Response(
                {'error': 'Strategy is already active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        strategy.is_active = True
        strategy.status = 'active'
        strategy.started_at = timezone.now()
        strategy.save()
        
        # Create alert
        StrategyAlert.objects.create(
            strategy=strategy,
            alert_type='custom',
            title='Strategy Started',
            message=f'Strategy "{strategy.name}" has been started',
            alert_data={'action': 'started'}
        )
        
        serializer = TradingStrategySerializer(strategy)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except TradingStrategy.DoesNotExist:
        return Response(
            {'error': 'Strategy not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def stop_strategy(request, strategy_id):
    """Stop a trading strategy"""
    try:
        strategy = TradingStrategy.objects.get(id=strategy_id, user=request.user)
        
        if not strategy.is_active:
            return Response(
                {'error': 'Strategy is not active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        strategy.is_active = False
        strategy.status = 'stopped'
        strategy.stopped_at = timezone.now()
        strategy.save()
        
        # Create alert
        StrategyAlert.objects.create(
            strategy=strategy,
            alert_type='custom',
            title='Strategy Stopped',
            message=f'Strategy "{strategy.name}" has been stopped',
            alert_data={'action': 'stopped'}
        )
        
        serializer = TradingStrategySerializer(strategy)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except TradingStrategy.DoesNotExist:
        return Response(
            {'error': 'Strategy not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def execute_strategy(request, strategy_id):
    """Execute a trading strategy manually"""
    try:
        strategy = TradingStrategy.objects.get(id=strategy_id, user=request.user)
        
        serializer = ExecuteStrategySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        dry_run = serializer.validated_data.get('dry_run', False)
        notes = serializer.validated_data.get('notes', '')
        
        # Simulate strategy execution based on strategy type
        execution_result = simulate_strategy_execution(strategy, dry_run)
        
        if dry_run:
            return Response({
                'message': 'Dry run completed',
                'strategy': TradingStrategySerializer(strategy).data,
                'execution_result': execution_result
            }, status=status.HTTP_200_OK)
        
        # Create execution record
        execution = StrategyExecution.objects.create(
            strategy=strategy,
            action=execution_result['action'],
            symbol=strategy.symbol,
            quantity=execution_result.get('quantity'),
            price=execution_result.get('price'),
            reason=execution_result['reason'],
            pnl=execution_result.get('pnl'),
            market_conditions=execution_result.get('market_conditions', {}),
            strategy_parameters=strategy.parameters
        )
        
        # Update strategy performance
        if execution_result.get('pnl'):
            strategy.total_pnl += execution_result['pnl']
            if execution_result['pnl'] > 0:
                strategy.winning_trades += 1
            else:
                strategy.losing_trades += 1
            strategy.total_trades += 1
        
        strategy.last_executed = timezone.now()
        strategy.save()
        
        return Response({
            'message': 'Strategy executed successfully',
            'execution_id': execution.id,
            'execution_result': execution_result
        }, status=status.HTTP_200_OK)
        
    except TradingStrategy.DoesNotExist:
        return Response(
            {'error': 'Strategy not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class StrategyAnalyticsView(APIView):
    """Get strategy analytics and performance metrics"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'strategy_id',
                openapi.IN_QUERY,
                description="Specific strategy ID",
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
        strategy_id = request.query_params.get('strategy_id')
        period = request.query_params.get('period', '30d')
        
        try:
            if strategy_id:
                strategies = TradingStrategy.objects.filter(
                    id=strategy_id, 
                    user=request.user
                )
            else:
                strategies = TradingStrategy.objects.filter(user=request.user)
            
            if not strategies.exists():
                return Response(
                    {'error': 'No strategies found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Calculate analytics for each strategy
            analytics_data = []
            total_pnl = Decimal('0')
            total_trades = 0
            
            for strategy in strategies:
                # Get performance records for the period
                if period != 'all':
                    start_date = get_period_start_date(period)
                    performance_records = StrategyPerformance.objects.filter(
                        strategy=strategy,
                        date__gte=start_date
                    )
                else:
                    performance_records = StrategyPerformance.objects.filter(strategy=strategy)
                
                # Calculate metrics
                latest_performance = performance_records.order_by('-date').first()
                
                analytics_data.append({
                    'strategy_id': strategy.id,
                    'strategy_name': strategy.name,
                    'strategy_type': strategy.strategy_type,
                    'total_pnl': strategy.total_pnl,
                    'total_trades': strategy.total_trades,
                    'win_rate': strategy.win_rate,
                    'max_drawdown': latest_performance.max_drawdown if latest_performance else 0,
                    'sharpe_ratio': latest_performance.sharpe_ratio if latest_performance else 0,
                    'is_active': strategy.is_active,
                    'last_executed': strategy.last_executed,
                    'created_at': strategy.created_at
                })
                
                total_pnl += strategy.total_pnl
                total_trades += strategy.total_trades
            
            return Response({
                'strategies': analytics_data,
                'portfolio_summary': {
                    'total_strategies': len(analytics_data),
                    'active_strategies': len([s for s in analytics_data if s['is_active']]),
                    'total_pnl': total_pnl,
                    'total_trades': total_trades,
                    'average_win_rate': sum(s['win_rate'] for s in analytics_data) / len(analytics_data) if analytics_data else 0
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def backtest_strategy(request, strategy_id):
    """Backtest a trading strategy"""
    try:
        strategy = TradingStrategy.objects.get(id=strategy_id, user=request.user)
        
        serializer = StrategyBacktestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        backtest_data = serializer.validated_data
        
        # Simulate backtest (in a real implementation, this would use historical data)
        backtest_results = simulate_backtest(strategy, backtest_data)
        
        return Response({
            'strategy': TradingStrategySerializer(strategy).data,
            'backtest_results': backtest_results
        }, status=status.HTTP_200_OK)
        
    except TradingStrategy.DoesNotExist:
        return Response(
            {'error': 'Strategy not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Helper functions
def simulate_strategy_execution(strategy, dry_run=False):
    """Simulate strategy execution based on strategy type"""
    # This is a simplified simulation - in a real implementation,
    # this would analyze market data and execute actual trades
    
    if strategy.strategy_type == 'dca':
        return {
            'action': 'buy',
            'quantity': Decimal('0.001'),
            'price': Decimal('50000'),
            'reason': 'DCA buy order executed',
            'pnl': Decimal('0'),
            'market_conditions': {'price': 50000, 'volume': 1000}
        }
    elif strategy.strategy_type == 'grid':
        return {
            'action': 'buy',
            'quantity': Decimal('0.01'),
            'price': Decimal('49500'),
            'reason': 'Grid buy order at lower level',
            'pnl': Decimal('5'),
            'market_conditions': {'price': 49500, 'volume': 2000}
        }
    elif strategy.strategy_type == 'momentum':
        return {
            'action': 'buy',
            'quantity': Decimal('0.005'),
            'price': Decimal('51000'),
            'reason': 'Momentum signal detected',
            'pnl': Decimal('2.5'),
            'market_conditions': {'price': 51000, 'volume': 1500}
        }
    else:
        return {
            'action': 'hold',
            'reason': 'No signal detected',
            'pnl': Decimal('0'),
            'market_conditions': {'price': 50000, 'volume': 1000}
        }


def simulate_backtest(strategy, backtest_data):
    """Simulate strategy backtesting"""
    # This is a simplified backtest simulation
    return {
        'start_date': backtest_data['start_date'],
        'end_date': backtest_data['end_date'],
        'initial_capital': backtest_data['initial_capital'],
        'final_capital': backtest_data['initial_capital'] * Decimal('1.15'),  # 15% return
        'total_return': Decimal('15.0'),
        'total_trades': 45,
        'winning_trades': 28,
        'losing_trades': 17,
        'win_rate': Decimal('62.22'),
        'max_drawdown': Decimal('8.5'),
        'sharpe_ratio': Decimal('1.8'),
        'volatility': Decimal('12.3')
    }


def get_period_start_date(period):
    """Get start date for a given period"""
    today = date.today()
    if period == '7d':
        return today - timedelta(days=7)
    elif period == '30d':
        return today - timedelta(days=30)
    elif period == '90d':
        return today - timedelta(days=90)
    elif period == '1y':
        return today - timedelta(days=365)
    else:
        return today - timedelta(days=30)
