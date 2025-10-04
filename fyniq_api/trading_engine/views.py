from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import TradingAlgorithmService
from risk_management.services import RiskManagementService
from compliance.services import ComplianceService
from .serializers import (
    PriceFeedSerializer, TradingSignalSerializer, ExecuteTradeSerializer,
    TradingStrategySerializer, OrderBookSerializer, MarketDataSerializer
)
from django.utils import timezone
import time

# Create your views here.

class PriceFeedView(APIView):
    """
    Get real-time price feed data.
    
    This endpoint provides real-time cryptocurrency price data including
    OHLCV (Open, High, Low, Close, Volume) information for trading decisions.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'symbol',
                openapi.IN_QUERY,
                description="Trading pair symbol (e.g., BTC/USD)",
                type=openapi.TYPE_STRING,
                default='BTC/USD'
            ),
            openapi.Parameter(
                'timeframe',
                openapi.IN_QUERY,
                description="Timeframe for price data",
                type=openapi.TYPE_STRING,
                enum=['1m', '5m', '15m', '1h', '4h', '1d'],
                default='1h'
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Number of data points to return",
                type=openapi.TYPE_INTEGER,
                default=100
            )
        ],
        responses={
            200: openapi.Response(
                description="Price feed data retrieved successfully",
                examples={
                    "application/json": {
                        "symbol": "BTC/USD",
                        "timestamp": "2024-01-01T12:00:00Z",
                        "open": "45000.00",
                        "high": "45100.00",
                        "low": "44900.00",
                        "close": "45050.00",
                        "volume": "100.5",
                        "change_24h": "2.5",
                        "change_percent": "0.056"
                    }
                }
            )
        },
        operation_description="Get real-time price feed data for trading"
    )
    def get(self, request):
        symbol = request.query_params.get('symbol', 'BTC/USD')
        timeframe = request.query_params.get('timeframe', '1h')
        limit = int(request.query_params.get('limit', 100))
        
        try:
            algo = TradingAlgorithmService()
            df = algo.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=limit)
            
            if df.empty:
                return Response({'error': 'No price data available'}, status=status.HTTP_404_NOT_FOUND)
            
            latest_data = df.tail(1).to_dict(orient="records")[0]
            latest_data['symbol'] = symbol
            latest_data['timeframe'] = timeframe
            
            return Response(latest_data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TradingSignalView(APIView):
    """
    Get trading signals from algorithms.
    
    This endpoint provides trading signals based on various technical analysis
    algorithms and market indicators to help with trading decisions.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'symbol',
                openapi.IN_QUERY,
                description="Trading pair symbol",
                type=openapi.TYPE_STRING,
                default='BTC/USD'
            ),
            openapi.Parameter(
                'strategy',
                openapi.IN_QUERY,
                description="Trading strategy to use",
                type=openapi.TYPE_STRING,
                enum=['rsi', 'macd', 'bollinger', 'moving_average', 'combined'],
                default='combined'
            )
        ],
        responses={
            200: openapi.Response(
                description="Trading signal generated successfully",
                examples={
                    "application/json": {
                        "signal": "buy",
                        "confidence": 0.85,
                        "symbol": "BTC/USD",
                        "current_price": "45000.00",
                        "target_price": "46000.00",
                        "stop_loss": "44000.00",
                        "indicators": {
                            "rsi": 35.5,
                            "macd": "positive",
                            "bollinger_position": "lower"
                        },
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            )
        },
        operation_description="Get trading signals from technical analysis algorithms"
    )
    def get(self, request):
        symbol = request.query_params.get('symbol', 'BTC/USD')
        strategy = request.query_params.get('strategy', 'combined')
        
        try:
            algo = TradingAlgorithmService()
            signal_data = algo.run_strategy(symbol=symbol, strategy=strategy)
            
            return Response(signal_data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExecuteTradeView(APIView):
    """
    Execute a trade order.
    
    This endpoint allows users to execute trades with risk management
    and compliance checks before order placement.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=ExecuteTradeSerializer,
        responses={
            200: openapi.Response(
                description="Trade executed successfully",
                examples={
                    "application/json": {
                        "status": "Trade executed successfully",
                        "order_id": "ORD123456789",
                        "symbol": "BTC/USD",
                        "side": "buy",
                        "amount": "0.001",
                        "price": "45000.00",
                        "total_value": "45.00",
                        "fee": "0.50",
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            ),
            400: "Bad Request - Validation errors or risk/compliance issues",
            403: "Forbidden - Insufficient permissions or KYC required"
        },
        operation_description="Execute a trade with risk and compliance checks"
    )
    def post(self, request):
        serializer = ExecuteTradeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        data = serializer.validated_data
        
        try:
            # Risk management checks
            risk = RiskManagementService()
            if not risk.check_position_size(data['amount']):
                return Response(
                    {"error": "Position size too large for risk limits"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not risk.check_leverage(data.get('leverage', 1)):
                return Response(
                    {"error": "Leverage too high for risk limits"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Compliance checks
            compliance = ComplianceService()
            if compliance.is_kyc_required(data['amount']) and not user.kyc_verified:
                return Response(
                    {"error": "KYC verification required for this trade amount"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Execute trade (simulated)
            order_id = f"ORD{user.id}{int(time.time())}"
            
            return Response({
                "status": "Trade executed successfully",
                "order_id": order_id,
                "symbol": data.get('symbol', 'BTC/USD'),
                "side": data['side'],
                "amount": str(data['amount']),
                "price": str(data.get('price', '45000.00')),
                "total_value": str(float(data['amount']) * float(data.get('price', 45000))),
                "fee": "0.50",
                "timestamp": timezone.now().isoformat()
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderBookView(APIView):
    """
    Get order book data.
    
    This endpoint provides the current order book showing buy and sell orders
    at different price levels for market depth analysis.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'symbol',
                openapi.IN_QUERY,
                description="Trading pair symbol",
                type=openapi.TYPE_STRING,
                default='BTC/USD'
            ),
            openapi.Parameter(
                'depth',
                openapi.IN_QUERY,
                description="Order book depth (number of levels)",
                type=openapi.TYPE_INTEGER,
                default=20
            )
        ],
        responses={
            200: openapi.Response(
                description="Order book data retrieved successfully",
                examples={
                    "application/json": {
                        "symbol": "BTC/USD",
                        "timestamp": "2024-01-01T12:00:00Z",
                        "bids": [
                            ["45000.00", "0.5"],
                            ["44999.00", "1.2"],
                            ["44998.00", "0.8"]
                        ],
                        "asks": [
                            ["45001.00", "0.3"],
                            ["45002.00", "0.7"],
                            ["45003.00", "1.1"]
                        ],
                        "spread": "1.00",
                        "spread_percent": "0.002"
                    }
                }
            )
        },
        operation_description="Get current order book data for market depth analysis"
    )
    def get(self, request):
        symbol = request.query_params.get('symbol', 'BTC/USD')
        depth = int(request.query_params.get('depth', 20))
        
        # Mock order book data
        order_book = {
            "symbol": symbol,
            "timestamp": timezone.now().isoformat(),
            "bids": [
                ["45000.00", "0.5"],
                ["44999.00", "1.2"],
                ["44998.00", "0.8"],
                ["44997.00", "0.9"],
                ["44996.00", "1.1"]
            ],
            "asks": [
                ["45001.00", "0.3"],
                ["45002.00", "0.7"],
                ["45003.00", "1.1"],
                ["45004.00", "0.6"],
                ["45005.00", "0.8"]
            ],
            "spread": "1.00",
            "spread_percent": "0.002"
        }
        
        return Response(order_book)

class MarketDataView(APIView):
    """
    Get comprehensive market data.
    
    This endpoint provides comprehensive market data including price,
    volume, market cap, and other key metrics for market analysis.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'symbol',
                openapi.IN_QUERY,
                description="Trading pair symbol",
                type=openapi.TYPE_STRING,
                default='BTC/USD'
            )
        ],
        responses={
            200: openapi.Response(
                description="Market data retrieved successfully",
                examples={
                    "application/json": {
                        "symbol": "BTC/USD",
                        "price": "45000.00",
                        "change_24h": "1250.00",
                        "change_percent_24h": "2.86",
                        "volume_24h": "25000000000",
                        "market_cap": "900000000000",
                        "circulating_supply": "19500000",
                        "max_supply": "21000000",
                        "high_24h": "45500.00",
                        "low_24h": "43500.00",
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            )
        },
        operation_description="Get comprehensive market data and statistics"
    )
    def get(self, request):
        symbol = request.query_params.get('symbol', 'BTC/USD')
        
        # Mock market data
        market_data = {
            "symbol": symbol,
            "price": "45000.00",
            "change_24h": "1250.00",
            "change_percent_24h": "2.86",
            "volume_24h": "25000000000",
            "market_cap": "900000000000",
            "circulating_supply": "19500000",
            "max_supply": "21000000",
            "high_24h": "45500.00",
            "low_24h": "43500.00",
            "timestamp": timezone.now().isoformat()
        }
        
        return Response(market_data)

class TradingStrategyView(APIView):
    """
    Configure and manage trading strategies.
    
    This endpoint allows users to configure, update, and manage their
    automated trading strategies and parameters.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=TradingStrategySerializer,
        responses={
            200: openapi.Response(
                description="Trading strategy configured successfully",
                examples={
                    "application/json": {
                        "strategy_id": "STR123456789",
                        "name": "RSI Strategy",
                        "symbol": "BTC/USD",
                        "parameters": {
                            "rsi_period": 14,
                            "rsi_oversold": 30,
                            "rsi_overbought": 70
                        },
                        "status": "active",
                        "created_at": "2024-01-01T12:00:00Z"
                    }
                }
            ),
            400: "Bad Request - Invalid strategy parameters"
        },
        operation_description="Configure and manage automated trading strategies"
    )
    def post(self, request):
        serializer = TradingStrategySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Mock strategy creation
        strategy_id = f"STR{request.user.id}{int(time.time())}"
        
        return Response({
            "strategy_id": strategy_id,
            "name": data['name'],
            "symbol": data['symbol'],
            "parameters": data['parameters'],
            "status": "active",
            "created_at": timezone.now().isoformat()
        })
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Trading strategies retrieved successfully",
                examples={
                    "application/json": {
                        "strategies": [
                            {
                                "strategy_id": "STR123456789",
                                "name": "RSI Strategy",
                                "symbol": "BTC/USD",
                                "status": "active",
                                "performance": {
                                    "total_trades": 25,
                                    "win_rate": 0.68,
                                    "profit_loss": "1250.00"
                                }
                            }
                        ]
                    }
                }
            )
        },
        operation_description="Get user's trading strategies"
    )
    def get(self, request):
        # Mock strategies data
        strategies = [
            {
                "strategy_id": f"STR{request.user.id}001",
                "name": "RSI Strategy",
                "symbol": "BTC/USD",
                "status": "active",
                "performance": {
                    "total_trades": 25,
                    "win_rate": 0.68,
                    "profit_loss": "1250.00"
                }
            }
        ]
        
        return Response({"strategies": strategies})
