"""
Advanced Trading Features - Order Types, Stop-Loss, Take-Profit, etc.
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from decimal import Decimal
from django.db import transaction
import json

from .models import AdvancedOrder, OrderType, TradingStrategy
from .serializers import (
    AdvancedOrderSerializer, OrderTypeSerializer, TradingStrategySerializer,
    StopLossOrderSerializer, TakeProfitOrderSerializer, LimitOrderSerializer,
    MarketOrderSerializer, StopLimitOrderSerializer
)
from .services import AdvancedTradingService, OrderManagementService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AdvancedOrderListView(generics.ListCreateAPIView):
    """List and create advanced orders"""
    serializer_class = AdvancedOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AdvancedOrder.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdvancedOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Manage individual advanced orders"""
    serializer_class = AdvancedOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AdvancedOrder.objects.filter(user=self.request.user)

class StopLossOrderView(APIView):
    """Create stop-loss orders"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=StopLossOrderSerializer,
        responses={
            201: openapi.Response(description="Stop-loss order created successfully"),
            400: openapi.Response(description="Invalid order data"),
            403: openapi.Response(description="Insufficient permissions or KYC required")
        }
    )
    def post(self, request):
        serializer = StopLossOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    order = AdvancedTradingService.create_stop_loss_order(
                        user=request.user,
                        **serializer.validated_data
                    )
                    return Response(
                        AdvancedOrderSerializer(order).data,
                        status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TakeProfitOrderView(APIView):
    """Create take-profit orders"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=TakeProfitOrderSerializer,
        responses={
            201: openapi.Response(description="Take-profit order created successfully"),
            400: openapi.Response(description="Invalid order data")
        }
    )
    def post(self, request):
        serializer = TakeProfitOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    order = AdvancedTradingService.create_take_profit_order(
                        user=request.user,
                        **serializer.validated_data
                    )
                    return Response(
                        AdvancedOrderSerializer(order).data,
                        status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LimitOrderView(APIView):
    """Create limit orders"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=LimitOrderSerializer,
        responses={
            201: openapi.Response(description="Limit order created successfully"),
            400: openapi.Response(description="Invalid order data")
        }
    )
    def post(self, request):
        serializer = LimitOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    order = AdvancedTradingService.create_limit_order(
                        user=request.user,
                        **serializer.validated_data
                    )
                    return Response(
                        AdvancedOrderSerializer(order).data,
                        status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarketOrderView(APIView):
    """Create market orders"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=MarketOrderSerializer,
        responses={
            201: openapi.Response(description="Market order created successfully"),
            400: openapi.Response(description="Invalid order data")
        }
    )
    def post(self, request):
        serializer = MarketOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    order = AdvancedTradingService.create_market_order(
                        user=request.user,
                        **serializer.validated_data
                    )
                    return Response(
                        AdvancedOrderSerializer(order).data,
                        status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StopLimitOrderView(APIView):
    """Create stop-limit orders"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=StopLimitOrderSerializer,
        responses={
            201: openapi.Response(description="Stop-limit order created successfully"),
            400: openapi.Response(description="Invalid order data")
        }
    )
    def post(self, request):
        serializer = StopLimitOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    order = AdvancedTradingService.create_stop_limit_order(
                        user=request.user,
                        **serializer.validated_data
                    )
                    return Response(
                        AdvancedOrderSerializer(order).data,
                        status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderManagementView(APIView):
    """Manage existing orders"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter by order status",
                type=openapi.TYPE_STRING,
                enum=['pending', 'filled', 'cancelled', 'expired']
            ),
            openapi.Parameter(
                'order_type',
                openapi.IN_QUERY,
                description="Filter by order type",
                type=openapi.TYPE_STRING,
                enum=['market', 'limit', 'stop_loss', 'take_profit', 'stop_limit']
            )
        ]
    )
    def get(self, request):
        """Get user's orders with optional filtering"""
        orders = AdvancedOrder.objects.filter(user=request.user)
        
        # Apply filters
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)
        
        order_type_filter = request.query_params.get('order_type')
        if order_type_filter:
            orders = orders.filter(order_type=order_type_filter)
        
        serializer = AdvancedOrderSerializer(orders, many=True)
        return Response({
            'orders': serializer.data,
            'count': orders.count()
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, order_id):
        """Cancel an order"""
        try:
            order = AdvancedOrder.objects.get(id=order_id, user=request.user)
            if order.status == 'pending':
                OrderManagementService.cancel_order(order)
                return Response(
                    {'message': 'Order cancelled successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Order cannot be cancelled'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except AdvancedOrder.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class TradingStrategyListView(generics.ListCreateAPIView):
    """List and create trading strategies"""
    serializer_class = TradingStrategySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TradingStrategy.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TradingStrategyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Manage individual trading strategies"""
    serializer_class = TradingStrategySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TradingStrategy.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def execute_strategy(request, strategy_id):
    """Execute a trading strategy"""
    try:
        strategy = TradingStrategy.objects.get(id=strategy_id, user=request.user)
        if not strategy.is_active:
            return Response(
                {'error': 'Strategy is not active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = AdvancedTradingService.execute_strategy(strategy)
        return Response({
            'message': 'Strategy executed successfully',
            'result': result
        }, status=status.HTTP_200_OK)
        
    except TradingStrategy.DoesNotExist:
        return Response(
            {'error': 'Strategy not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def order_history(request):
    """Get order history with pagination"""
    orders = AdvancedOrder.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    
    orders_page = orders[start:end]
    serializer = AdvancedOrderSerializer(orders_page, many=True)
    
    return Response({
        'orders': serializer.data,
        'page': page,
        'page_size': page_size,
        'total_count': orders.count(),
        'has_next': end < orders.count(),
        'has_previous': page > 1
    }, status=status.HTTP_200_OK)
