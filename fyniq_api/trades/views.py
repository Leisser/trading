from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Trade
from .serializers import TradeSerializer, TradeCreateSerializer, TradeStatsSerializer

class TradeListCreateView(generics.ListCreateAPIView):
    """
    List and create trades.
    
    This endpoint allows authenticated users to view their trading history
    and create new trades. Trades are filtered by the authenticated user.
    """
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user).order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
                default=1
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER,
                default=20
            ),
            openapi.Parameter(
                'trade_type',
                openapi.IN_QUERY,
                description="Filter by trade type (buy/sell)",
                type=openapi.TYPE_STRING,
                enum=['buy', 'sell']
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter by trade status",
                type=openapi.TYPE_STRING,
                enum=['pending', 'completed', 'cancelled', 'failed']
            )
        ],
        responses={
            200: openapi.Response(
                description="Trades retrieved successfully",
                examples={
                    "application/json": {
                        "count": 50,
                        "next": "http://localhost:8000/api/trades/?page=2",
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "trade_type": "buy",
                                "amount": "0.001",
                                "price": "45000.00",
                                "total_value": "45.00",
                                "status": "completed",
                                "timestamp": "2024-01-01T12:00:00Z"
                            }
                        ]
                    }
                }
            )
        },
        operation_description="Get paginated list of user's trades with optional filtering"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        request_body=TradeCreateSerializer,
        responses={
            201: openapi.Response(
                description="Trade created successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "trade_type": "buy",
                        "amount": "0.001",
                        "price": "45000.00",
                        "total_value": "45.00",
                        "status": "pending",
                        "timestamp": "2024-01-01T12:00:00Z",
                        "message": "Trade created successfully"
                    }
                }
            ),
            400: "Bad Request - Validation errors"
        },
        operation_description="Create a new trade"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific trade.
    
    This endpoint allows users to view details of a specific trade,
    update trade information, or cancel a trade.
    """
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)
    
    @swagger_auto_schema(
        responses={
            200: TradeSerializer,
            404: "Trade not found"
        },
        operation_description="Get details of a specific trade"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        request_body=TradeSerializer,
        responses={
            200: openapi.Response(
                description="Trade updated successfully",
                examples={
                    "application/json": {
                        "message": "Trade updated successfully",
                        "trade": {
                            "id": 1,
                            "trade_type": "buy",
                            "amount": "0.002",
                            "price": "45000.00",
                            "status": "pending"
                        }
                    }
                }
            ),
            400: "Bad Request - Validation errors"
        },
        operation_description="Update a specific trade"
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        responses={
            204: "Trade deleted successfully",
            404: "Trade not found"
        },
        operation_description="Delete a specific trade"
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class TradeStatsView(APIView):
    """
    Get trading statistics and analytics.
    
    This endpoint provides comprehensive trading statistics including
    total volume, profit/loss, win rate, and other key metrics.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'period',
                openapi.IN_QUERY,
                description="Time period for statistics",
                type=openapi.TYPE_STRING,
                enum=['day', 'week', 'month', 'year', 'all'],
                default='month'
            )
        ],
        responses={
            200: openapi.Response(
                description="Trading statistics retrieved successfully",
                examples={
                    "application/json": {
                        "total_trades": 150,
                        "total_volume": "0.500",
                        "total_value": "22500.00",
                        "profit_loss": "1250.00",
                        "win_rate": 0.65,
                        "average_trade_size": "0.003",
                        "largest_trade": "0.010",
                        "most_active_day": "2024-01-15",
                        "buy_trades": 80,
                        "sell_trades": 70
                    }
                }
            )
        },
        operation_description="Get comprehensive trading statistics"
    )
    def get(self, request):
        # Mock statistics for demonstration
        stats = {
            'total_trades': 150,
            'total_volume': '0.500',
            'total_value': '22500.00',
            'profit_loss': '1250.00',
            'win_rate': 0.65,
            'average_trade_size': '0.003',
            'largest_trade': '0.010',
            'most_active_day': '2024-01-15',
            'buy_trades': 80,
            'sell_trades': 70
        }
        return Response(stats)

class CancelTradeView(APIView):
    """
    Cancel a pending trade.
    
    This endpoint allows users to cancel trades that are still pending
    and haven't been executed yet.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Trade cancelled successfully",
                examples={
                    "application/json": {
                        "message": "Trade cancelled successfully",
                        "trade_id": 1,
                        "status": "cancelled"
                    }
                }
            ),
            400: "Trade cannot be cancelled",
            404: "Trade not found"
        },
        operation_description="Cancel a pending trade"
    )
    def post(self, request, trade_id):
        trade = get_object_or_404(Trade, id=trade_id, user=request.user)
        
        if trade.status != 'pending':
            return Response(
                {'error': 'Only pending trades can be cancelled'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trade.status = 'cancelled'
        trade.save()
        
        return Response({
            'message': 'Trade cancelled successfully',
            'trade_id': trade.id,
            'status': trade.status
        })

class TradeHistoryView(generics.ListAPIView):
    """
    Get detailed trade history with advanced filtering.
    
    This endpoint provides a comprehensive view of trading history
    with advanced filtering and sorting options.
    """
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Trade.objects.filter(user=self.request.user)
        
        # Apply filters
        trade_type = self.request.query_params.get('trade_type')
        if trade_type:
            queryset = queryset.filter(trade_type=trade_type)
        
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        
        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset.order_by('-timestamp')
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'trade_type',
                openapi.IN_QUERY,
                description="Filter by trade type",
                type=openapi.TYPE_STRING,
                enum=['buy', 'sell']
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter by trade status",
                type=openapi.TYPE_STRING,
                enum=['pending', 'completed', 'cancelled', 'failed']
            ),
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Start date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="End date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
                default=1
            )
        ],
        responses={
            200: openapi.Response(
                description="Trade history retrieved successfully",
                examples={
                    "application/json": {
                        "count": 100,
                        "next": "http://localhost:8000/api/trades/history/?page=2",
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "trade_type": "buy",
                                "amount": "0.001",
                                "price": "45000.00",
                                "total_value": "45.00",
                                "status": "completed",
                                "timestamp": "2024-01-01T12:00:00Z",
                                "fee": "0.50"
                            }
                        ]
                    }
                }
            )
        },
        operation_description="Get detailed trade history with advanced filtering"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) 