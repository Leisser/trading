from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
import logging

from trades.models import Trade
from accounts.models import User

logger = logging.getLogger(__name__)
User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_stats(request):
    """
    Get dashboard statistics.
    """
    try:
        # Mock dashboard statistics for now
        stats = {
            'total_portfolio_value': 2845672.50,
            'portfolio_change': 12.5,
            'active_trades': 1247,
            'new_trades_today': 89,
            'active_users': 15673,
            'user_growth': 8.2,
            'system_health': 99.2
        }
        
        return Response(stats, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Dashboard stats error: {str(e)}")
        return Response(
            {'error': 'Failed to fetch dashboard statistics'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def user_stats(request):
    """
    Get user statistics.
    """
    try:
        stats = {
            'total_users': 15673,
            'active_users': 12450,
            'growth_rate': 8.2
        }
        
        return Response(stats, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"User stats error: {str(e)}")
        return Response(
            {'error': 'Failed to fetch user statistics'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def recent_trades(request):
    """
    Get recent trades.
    """
    try:
        # Mock recent trades data
        trades = [
            {
                'id': 1,
                'pair': 'BTC/USD',
                'amount': '12450.00',
                'trade_type': 'buy',
                'status': 'completed',
                'created_at': '2025-01-04T11:20:00Z'
            },
            {
                'id': 2,
                'pair': 'ETH/USD',
                'amount': '8920.00',
                'trade_type': 'sell',
                'status': 'completed',
                'created_at': '2025-01-04T11:15:00Z'
            },
            {
                'id': 3,
                'pair': 'ADA/USD',
                'amount': '3456.00',
                'trade_type': 'buy',
                'status': 'completed',
                'created_at': '2025-01-04T11:10:00Z'
            },
            {
                'id': 4,
                'pair': 'DOT/USD',
                'amount': '5678.00',
                'trade_type': 'sell',
                'status': 'completed',
                'created_at': '2025-01-04T11:05:00Z'
            }
        ]
        
        return Response(trades, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Recent trades error: {str(e)}")
        return Response(
            {'error': 'Failed to fetch recent trades'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
