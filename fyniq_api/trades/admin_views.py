from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Avg, Q, Count
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta
import random
import time

from .models import (
    TradingSettings, ProfitLossScenario, DepositWallet, UserDepositRequest,
    PriceMovementLog, AutomatedTask, CryptoIndex, Cryptocurrency, CryptoInvestment
)
from .serializers import (
    TradingSettingsSerializer, ProfitLossScenarioSerializer, DepositWalletSerializer,
    UserDepositRequestSerializer, PriceMovementLogSerializer, AutomatedTaskSerializer
)


class AdminTradingSettingsView(generics.RetrieveUpdateAPIView):
    """Get and update global trading settings (Admin only)"""
    serializer_class = TradingSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_object(self):
        # Get or create the single trading settings instance
        settings, created = TradingSettings.objects.get_or_create(id=1)
        return settings


class ProfitLossScenarioListView(generics.ListCreateAPIView):
    """List and create profit/loss scenarios (Admin only)"""
    serializer_class = ProfitLossScenarioSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        return ProfitLossScenario.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProfitLossScenarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific profit/loss scenario (Admin only)"""
    queryset = ProfitLossScenario.objects.all()
    serializer_class = ProfitLossScenarioSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def execute_scenario(request, scenario_id):
    """Manually execute a profit/loss scenario"""
    scenario = get_object_or_404(ProfitLossScenario, id=scenario_id)
    
    try:
        # Execute the scenario immediately
        result = execute_profit_loss_scenario(scenario)
        
        # Update scenario execution tracking
        scenario.times_executed += 1
        scenario.last_executed = timezone.now()
        scenario.save()
        
        return Response({
            'success': True,
            'message': f'Scenario "{scenario.name}" executed successfully',
            'affected_investments': result.get('affected_count', 0),
            'price_changes': result.get('price_changes', [])
        })
    
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def manual_price_control(request):
    """Manually control cryptocurrency or index prices"""
    crypto_id = request.data.get('cryptocurrency_id')
    index_id = request.data.get('crypto_index_id')
    price_change_percent = request.data.get('price_change_percent', 0)
    duration_seconds = request.data.get('duration_seconds', 1)
    
    if not crypto_id and not index_id:
        return Response({
            'error': 'Either cryptocurrency_id or crypto_index_id must be provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        results = []
        
        if crypto_id:
            crypto = get_object_or_404(Cryptocurrency, id=crypto_id)
            result = apply_price_change(crypto, price_change_percent, duration_seconds, 'admin_controlled')
            results.append(result)
        
        if index_id:
            index = get_object_or_404(CryptoIndex, id=index_id)
            result = apply_index_price_change(index, price_change_percent, duration_seconds, 'admin_controlled')
            results.append(result)
        
        return Response({
            'success': True,
            'message': 'Price changes applied successfully',
            'results': results
        })
    
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


class DepositWalletListView(generics.ListCreateAPIView):
    """List and create deposit wallets (Admin only)"""
    queryset = DepositWallet.objects.all()
    serializer_class = DepositWalletSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DepositWalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a deposit wallet (Admin only)"""
    queryset = DepositWallet.objects.all()
    serializer_class = DepositWalletSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class PendingDepositsView(generics.ListAPIView):
    """List pending deposit requests for admin review"""
    serializer_class = UserDepositRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        return UserDepositRequest.objects.filter(status='pending').select_related('user', 'deposit_wallet')


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def approve_deposit(request, deposit_id):
    """Approve a pending deposit request"""
    deposit = get_object_or_404(UserDepositRequest, id=deposit_id)
    
    if deposit.status != 'pending':
        return Response({
            'error': 'Deposit is not in pending status'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Update deposit status
    deposit.status = 'confirmed'
    deposit.reviewed_by = request.user
    deposit.reviewed_at = timezone.now()
    deposit.confirmed_at = timezone.now()
    deposit.review_notes = request.data.get('notes', '')
    deposit.save()
    
    # Update user's wallet balance or create investment
    # This would integrate with your existing wallet/investment system
    
    return Response({
        'success': True,
        'message': 'Deposit approved successfully',
        'deposit': UserDepositRequestSerializer(deposit).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def reject_deposit(request, deposit_id):
    """Reject a pending deposit request"""
    deposit = get_object_or_404(UserDepositRequest, id=deposit_id)
    
    if deposit.status != 'pending':
        return Response({
            'error': 'Deposit is not in pending status'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Update deposit status
    deposit.status = 'rejected'
    deposit.reviewed_by = request.user
    deposit.reviewed_at = timezone.now()
    deposit.review_notes = request.data.get('notes', 'Rejected by admin')
    deposit.save()
    
    return Response({
        'success': True,
        'message': 'Deposit rejected',
        'deposit': UserDepositRequestSerializer(deposit).data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_dashboard_stats(request):
    """Get comprehensive admin dashboard statistics"""
    
    # Trading Statistics
    total_investments = CryptoInvestment.objects.count()
    active_investments = CryptoInvestment.objects.filter(status='active').count()
    total_portfolio_value = CryptoInvestment.objects.filter(status='active').aggregate(
        total=Sum('current_value_btc')
    )['total'] or 0
    
    # Deposit Statistics
    pending_deposits = UserDepositRequest.objects.filter(status='pending').count()
    total_deposits_today = UserDepositRequest.objects.filter(
        created_at__gte=timezone.now().replace(hour=0, minute=0, second=0)
    ).count()
    total_deposit_value = UserDepositRequest.objects.filter(status='confirmed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Price Movement Statistics
    price_movements_today = PriceMovementLog.objects.filter(
        timestamp__gte=timezone.now().replace(hour=0, minute=0, second=0)
    ).count()
    
    admin_controlled_movements = PriceMovementLog.objects.filter(
        movement_type='admin_controlled',
        timestamp__gte=timezone.now() - timedelta(hours=24)
    ).count()
    
    # Task Statistics
    completed_tasks_today = AutomatedTask.objects.filter(
        status='completed',
        completed_at__gte=timezone.now().replace(hour=0, minute=0, second=0)
    ).count()
    
    failed_tasks_today = AutomatedTask.objects.filter(
        status='failed',
        created_at__gte=timezone.now().replace(hour=0, minute=0, second=0)
    ).count()
    
    # Active Scenarios
    active_scenarios = ProfitLossScenario.objects.filter(is_active=True).count()
    
    return Response({
        'trading_stats': {
            'total_investments': total_investments,
            'active_investments': active_investments,
            'total_portfolio_value_btc': float(total_portfolio_value),
        },
        'deposit_stats': {
            'pending_deposits': pending_deposits,
            'deposits_today': total_deposits_today,
            'total_deposit_value_btc': float(total_deposit_value),
        },
        'price_movement_stats': {
            'movements_today': price_movements_today,
            'admin_controlled_today': admin_controlled_movements,
        },
        'task_stats': {
            'completed_tasks_today': completed_tasks_today,
            'failed_tasks_today': failed_tasks_today,
        },
        'scenario_stats': {
            'active_scenarios': active_scenarios,
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def recent_price_movements(request):
    """Get recent price movements with filtering"""
    hours = int(request.GET.get('hours', 24))
    movement_type = request.GET.get('movement_type', '')
    
    queryset = PriceMovementLog.objects.filter(
        timestamp__gte=timezone.now() - timedelta(hours=hours)
    )
    
    if movement_type:
        queryset = queryset.filter(movement_type=movement_type)
    
    movements = queryset.select_related(
        'cryptocurrency', 'crypto_index', 'triggered_by_scenario'
    )[:100]  # Limit to 100 recent movements
    
    serializer = PriceMovementLogSerializer(movements, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def system_health_check(request):
    """Check system health and task status"""
    
    # Check recent task execution
    recent_tasks = AutomatedTask.objects.filter(
        created_at__gte=timezone.now() - timedelta(minutes=5)
    )
    
    task_health = {
        'price_updates': recent_tasks.filter(task_type='price_update').exists(),
        'investment_calculations': recent_tasks.filter(task_type='investment_calculation').exists(),
        'portfolio_updates': recent_tasks.filter(task_type='portfolio_update').exists(),
    }
    
    # Check for stuck tasks
    stuck_tasks = AutomatedTask.objects.filter(
        status='running',
        started_at__lte=timezone.now() - timedelta(minutes=10)
    ).count()
    
    # Check trading settings
    trading_settings = TradingSettings.objects.first()
    
    return Response({
        'system_status': {
            'trading_enabled': trading_settings.trading_enabled if trading_settings else False,
            'maintenance_mode': trading_settings.maintenance_mode if trading_settings else True,
            'stuck_tasks': stuck_tasks,
        },
        'task_health': task_health,
        'last_updated': timezone.now()
    })


# Helper Functions for Price Control
def execute_profit_loss_scenario(scenario):
    """Execute a profit/loss scenario"""
    results = {
        'affected_count': 0,
        'price_changes': []
    }
    
    # Determine targets
    targets = []
    if scenario.target_cryptocurrency:
        targets.append(('crypto', scenario.target_cryptocurrency))
    elif scenario.target_crypto_index:
        targets.append(('index', scenario.target_crypto_index))
    elif scenario.apply_to_all_investments:
        # Apply to all active cryptocurrencies and indices
        for crypto in Cryptocurrency.objects.filter(is_active=True):
            targets.append(('crypto', crypto))
        for index in CryptoIndex.objects.filter(is_active=True):
            targets.append(('index', index))
    
    # Apply price changes
    for target_type, target_obj in targets:
        try:
            if target_type == 'crypto':
                result = apply_price_change(
                    target_obj, 
                    scenario.percentage_change, 
                    scenario.duration_in_seconds,
                    'scenario_based',
                    scenario
                )
            else:  # index
                result = apply_index_price_change(
                    target_obj, 
                    scenario.percentage_change, 
                    scenario.duration_in_seconds,
                    'scenario_based',
                    scenario
                )
            
            results['price_changes'].append(result)
            results['affected_count'] += 1
            
        except Exception as e:
            print(f"Error applying scenario to {target_obj}: {e}")
    
    return results


def apply_price_change(cryptocurrency, percentage_change, duration_seconds, movement_type='admin_controlled', scenario=None):
    """Apply price change to a cryptocurrency"""
    old_price = cryptocurrency.current_price
    
    # Calculate new price
    change_multiplier = 1 + (percentage_change / 100)
    new_price = old_price * Decimal(str(change_multiplier))
    
    # Update cryptocurrency price
    cryptocurrency.current_price = new_price
    cryptocurrency.price_change_24h = percentage_change
    cryptocurrency.save()
    
    # Log the price movement
    price_change = new_price - old_price
    PriceMovementLog.objects.create(
        cryptocurrency=cryptocurrency,
        previous_price=old_price,
        new_price=new_price,
        price_change=price_change,
        price_change_percent=percentage_change,
        movement_type=movement_type,
        triggered_by_scenario=scenario,
        notes=f"Applied {percentage_change}% change over {duration_seconds} seconds"
    )
    
    # Update related investments
    update_crypto_investments(cryptocurrency, percentage_change)
    
    return {
        'target': f"{cryptocurrency.symbol}",
        'old_price': float(old_price),
        'new_price': float(new_price),
        'change_percent': float(percentage_change)
    }


def apply_index_price_change(crypto_index, percentage_change, duration_seconds, movement_type='admin_controlled', scenario=None):
    """Apply price change to a crypto index"""
    old_value = crypto_index.current_value
    
    # Calculate new value
    change_multiplier = 1 + (percentage_change / 100)
    new_value = old_value * Decimal(str(change_multiplier))
    
    # Update index value
    crypto_index.current_value = new_value
    crypto_index.price_change_24h = percentage_change
    crypto_index.save()
    
    # Log the price movement
    value_change = new_value - old_value
    PriceMovementLog.objects.create(
        crypto_index=crypto_index,
        previous_price=old_value,
        new_price=new_value,
        price_change=value_change,
        price_change_percent=percentage_change,
        movement_type=movement_type,
        triggered_by_scenario=scenario,
        notes=f"Applied {percentage_change}% change over {duration_seconds} seconds"
    )
    
    # Update related investments
    update_index_investments(crypto_index, percentage_change)
    
    return {
        'target': f"{crypto_index.symbol} Index",
        'old_value': float(old_value),
        'new_value': float(new_value),
        'change_percent': float(percentage_change)
    }


def update_crypto_investments(cryptocurrency, percentage_change):
    """Update investments related to a cryptocurrency"""
    investments = CryptoInvestment.objects.filter(
        cryptocurrency=cryptocurrency,
        status='active'
    )
    
    change_multiplier = 1 + (percentage_change / 100)
    
    for investment in investments:
        # Update current value
        investment.current_value_btc *= Decimal(str(change_multiplier))
        investment.current_value_usd *= Decimal(str(change_multiplier))
        
        # Recalculate P&L
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


def update_index_investments(crypto_index, percentage_change):
    """Update investments related to a crypto index"""
    investments = CryptoInvestment.objects.filter(
        crypto_index=crypto_index,
        status='active'
    )
    
    change_multiplier = 1 + (percentage_change / 100)
    
    for investment in investments:
        # Update current value
        investment.current_value_btc *= Decimal(str(change_multiplier))
        investment.current_value_usd *= Decimal(str(change_multiplier))
        
        # Recalculate P&L
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