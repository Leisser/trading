"""
Market Data API Views for real-time cryptocurrency data.
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from decimal import Decimal
import json

from .models import Exchange, TradingPair, MarketData, PriceAlert
from .services import MarketDataService, PriceAlertService, TechnicalAnalysisService
from .serializers import (
    MarketDataSerializer, TradingPairSerializer, ExchangeSerializer,
    PriceAlertSerializer, TechnicalAnalysisSerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_cryptocurrencies(request):
    """
    Get list of cryptocurrencies with current prices.
    """
    try:
        # Mock cryptocurrency data for now
        cryptocurrencies = [
            {
                'symbol': 'BTC',
                'name': 'Bitcoin',
                'price': '45234.56',
                'change_24h': 5.2
            },
            {
                'symbol': 'ETH',
                'name': 'Ethereum',
                'price': '3187.92',
                'change_24h': 3.8
            },
            {
                'symbol': 'ADA',
                'name': 'Cardano',
                'price': '0.89',
                'change_24h': -2.1
            },
            {
                'symbol': 'DOT',
                'name': 'Polkadot',
                'price': '23.45',
                'change_24h': 7.3
            },
            {
                'symbol': 'SOL',
                'name': 'Solana',
                'price': '112.78',
                'change_24h': -1.5
            }
        ]
        
        return Response(cryptocurrencies, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch cryptocurrency data'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class RealTimePriceView(APIView):
    """Get real-time price for a trading pair"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'symbol',
                openapi.IN_QUERY,
                description="Trading pair symbol (e.g., BTC/USDT)",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'exchange',
                openapi.IN_QUERY,
                description="Exchange name (binance, coinbase, kraken)",
                type=openapi.TYPE_STRING,
                default='binance'
            )
        ],
        responses={
            200: openapi.Response(
                description="Real-time price data",
                examples={
                    "application/json": {
                        "symbol": "BTC/USDT",
                        "exchange": "binance",
                        "price": "45000.00",
                        "bid": "44995.50",
                        "ask": "45004.50",
                        "volume": "1250.75",
                        "change_24h": "1250.00",
                        "change_percent_24h": "2.85",
                        "high_24h": "45500.00",
                        "low_24h": "43750.00",
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            )
        }
    )
    def get(self, request):
        symbol = request.query_params.get('symbol', 'BTC/USDT')
        exchange = request.query_params.get('exchange', 'binance')
        
        service = MarketDataService()
        price_data = service.get_real_time_price(symbol, exchange)
        
        if price_data:
            return Response(price_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Failed to fetch price data'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class OHLCVDataView(APIView):
    """Get OHLCV (candlestick) data for a trading pair"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'symbol',
                openapi.IN_QUERY,
                description="Trading pair symbol",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'timeframe',
                openapi.IN_QUERY,
                description="Timeframe (1m, 5m, 15m, 1h, 4h, 1d)",
                type=openapi.TYPE_STRING,
                default='1h'
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Number of candles to return",
                type=openapi.TYPE_INTEGER,
                default=100
            ),
            openapi.Parameter(
                'exchange',
                openapi.IN_QUERY,
                description="Exchange name",
                type=openapi.TYPE_STRING,
                default='binance'
            )
        ]
    )
    def get(self, request):
        symbol = request.query_params.get('symbol', 'BTC/USDT')
        timeframe = request.query_params.get('timeframe', '1h')
        limit = int(request.query_params.get('limit', 100))
        exchange = request.query_params.get('exchange', 'binance')
        
        service = MarketDataService()
        ohlcv_data = service.get_ohlcv_data(symbol, timeframe, limit, exchange)
        
        return Response({
            'symbol': symbol,
            'timeframe': timeframe,
            'exchange': exchange,
            'data': ohlcv_data,
            'count': len(ohlcv_data)
        }, status=status.HTTP_200_OK)

class OrderBookView(APIView):
    """Get order book data for a trading pair"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'symbol',
                openapi.IN_QUERY,
                description="Trading pair symbol",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'exchange',
                openapi.IN_QUERY,
                description="Exchange name",
                type=openapi.TYPE_STRING,
                default='binance'
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Number of orders to return",
                type=openapi.TYPE_INTEGER,
                default=20
            )
        ]
    )
    def get(self, request):
        symbol = request.query_params.get('symbol', 'BTC/USDT')
        exchange = request.query_params.get('exchange', 'binance')
        limit = int(request.query_params.get('limit', 20))
        
        service = MarketDataService()
        order_book = service.get_order_book(symbol, exchange, limit)
        
        if order_book:
            return Response(order_book, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Failed to fetch order book'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TradingPairsView(APIView):
    """Get available trading pairs from exchanges"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'exchange',
                openapi.IN_QUERY,
                description="Exchange name",
                type=openapi.TYPE_STRING,
                default='binance'
            )
        ]
    )
    def get(self, request):
        exchange = request.query_params.get('exchange', 'binance')
        
        service = MarketDataService()
        pairs = service.get_trading_pairs(exchange)
        
        return Response({
            'exchange': exchange,
            'pairs': pairs,
            'count': len(pairs)
        }, status=status.HTTP_200_OK)

class PriceAlertListView(generics.ListCreateAPIView):
    """List and create price alerts"""
    serializer_class = PriceAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PriceAlert.objects.filter(user=self.request.user, is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PriceAlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Manage individual price alerts"""
    serializer_class = PriceAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PriceAlert.objects.filter(user=self.request.user)

class TechnicalAnalysisView(APIView):
    """Get technical analysis indicators"""
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'symbol',
                openapi.IN_QUERY,
                description="Trading pair symbol",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'timeframe',
                openapi.IN_QUERY,
                description="Timeframe for analysis",
                type=openapi.TYPE_STRING,
                default='1h'
            ),
            openapi.Parameter(
                'period',
                openapi.IN_QUERY,
                description="Period for indicators",
                type=openapi.TYPE_INTEGER,
                default=14
            ),
            openapi.Parameter(
                'exchange',
                openapi.IN_QUERY,
                description="Exchange name",
                type=openapi.TYPE_STRING,
                default='binance'
            )
        ]
    )
    def get(self, request):
        symbol = request.query_params.get('symbol', 'BTC/USDT')
        timeframe = request.query_params.get('timeframe', '1h')
        period = int(request.query_params.get('period', 14))
        exchange = request.query_params.get('exchange', 'binance')
        
        # Get OHLCV data
        service = MarketDataService()
        ohlcv_data = service.get_ohlcv_data(symbol, timeframe, 200, exchange)
        
        if not ohlcv_data:
            return Response(
                {'error': 'Failed to fetch market data'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Extract close prices
        close_prices = [candle['close'] for candle in ohlcv_data]
        
        # Calculate technical indicators
        rsi = TechnicalAnalysisService.calculate_rsi(close_prices, period)
        sma_20 = TechnicalAnalysisService.calculate_sma(close_prices, 20)
        sma_50 = TechnicalAnalysisService.calculate_sma(close_prices, 50)
        ema_12 = TechnicalAnalysisService.calculate_ema(close_prices, 12)
        ema_26 = TechnicalAnalysisService.calculate_ema(close_prices, 26)
        
        return Response({
            'symbol': symbol,
            'timeframe': timeframe,
            'period': period,
            'indicators': {
                'rsi': rsi[-10:] if rsi else [],  # Last 10 RSI values
                'sma_20': sma_20[-10:] if sma_20 else [],
                'sma_50': sma_50[-10:] if sma_50 else [],
                'ema_12': ema_12[-10:] if ema_12 else [],
                'ema_26': ema_26[-10:] if ema_26 else []
            },
            'current_price': close_prices[-1] if close_prices else None,
            'timestamp': timezone.now()
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def sync_market_data(request):
    """Sync market data from exchanges to database"""
    symbol = request.data.get('symbol', 'BTC/USDT')
    timeframe = request.data.get('timeframe', '1h')
    exchange = request.data.get('exchange', 'binance')
    
    service = MarketDataService()
    ohlcv_data = service.get_ohlcv_data(symbol, timeframe, 100, exchange)
    
    if ohlcv_data:
        service.store_market_data(symbol, ohlcv_data, exchange)
        return Response({
            'message': f'Successfully synced {len(ohlcv_data)} records for {symbol}',
            'symbol': symbol,
            'exchange': exchange,
            'records_synced': len(ohlcv_data)
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Failed to fetch market data'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )