"""
API views for serving market data to frontend charts
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from trades.models import Cryptocurrency
from .models import MarketDataSimulation, UserTradeOutcome, TradingSettings
from .price_simulator import ActiveTradeManager
from .real_price_service import get_price_service
from market_data.models import ChartDataPoint


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_live_chart_data(request):
    """
    Get live chart data for a cryptocurrency
    Returns OHLCV data for candlestick and line charts
    
    Query params:
    - symbol: Cryptocurrency symbol (default: BTC)
    - limit: Number of data points (default: 30)
    """
    try:
        symbol = request.query_params.get('symbol', 'BTC')
        limit = int(request.query_params.get('limit', 30))
        
        # Get cryptocurrency
        try:
            crypto = Cryptocurrency.objects.get(symbol=symbol)
            current_price = float(crypto.current_price)
        except Cryptocurrency.DoesNotExist:
            current_price = 43250.0  # Default
        
        # Check if there's an active trade for this cryptocurrency
        active_outcome = UserTradeOutcome.objects.filter(
            is_executed=False,
            trade__cryptocurrency__symbol=symbol,
            trade__trade_type='buy'
        ).select_related('trade').order_by('created_at').first()
        
        if active_outcome:
            # Generate realistic price path based on predetermined outcome
            simulator, elapsed = ActiveTradeManager.get_active_trade_simulator(active_outcome)
            
            if simulator:
                # Generate candlestick data
                candles = simulator.generate_candlestick_data(interval_seconds=120)  # 2-minute candles
                
                # Take last N candles
                candles = candles[-limit:]
                
                return Response({
                    'symbol': symbol,
                    'current_price': float(active_outcome.trade.cryptocurrency.current_price),
                    'entry_price': float(active_outcome.trade.price),
                    'expected_outcome': active_outcome.outcome,
                    'expected_percentage': float(active_outcome.outcome_percentage),
                    'duration_seconds': active_outcome.duration_seconds,
                    'elapsed_seconds': int(elapsed),
                    'remaining_seconds': int((active_outcome.target_close_time - timezone.now()).total_seconds()),
                    'has_active_trade': True,
                    'chart_data': candles
                })
        
        # No active trade - get historical market data
        historical_data = MarketDataSimulation.objects.filter(
            cryptocurrency_symbol=symbol
        ).order_by('-timestamp')[:limit]
        
        candles = []
        for data in reversed(historical_data):
            candles.append({
                'timestamp': int(data.timestamp.timestamp()),
                'open': float(data.open_price),
                'high': float(data.high_price),
                'low': float(data.low_price),
                'close': float(data.close_price),
                'volume': float(data.volume)
            })
        
        # If no historical data, generate mock data
        if not candles:
            import random
            for i in range(limit):
                time_offset = i * 120  # 2 minutes apart
                price_change = random.uniform(-0.02, 0.02)
                price = current_price * (1 + price_change)
                
                candles.append({
                    'timestamp': int((timezone.now() - timedelta(seconds=(limit - i) * 120)).timestamp()),
                    'open': price * 0.999,
                    'high': price * 1.003,
                    'low': price * 0.997,
                    'close': price,
                    'volume': random.uniform(100000, 500000)
                })
        
        return Response({
            'symbol': symbol,
            'current_price': current_price,
            'has_active_trade': False,
            'chart_data': candles
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=500
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_price_update(request):
    """
    Get current price for a cryptocurrency with realistic movement
    Called frequently by frontend for live updates
    
    Query params:
    - symbol: Cryptocurrency symbol
    """
    try:
        symbol = request.query_params.get('symbol', 'BTC')
        
        # Check for active trade
        active_outcome = UserTradeOutcome.objects.filter(
            is_executed=False,
            trade__cryptocurrency__symbol=symbol,
            trade__trade_type='buy'
        ).select_related('trade', 'trade__cryptocurrency').order_by('created_at').first()
        
        if active_outcome:
            # Get simulated price from predetermined path
            simulated_price = ActiveTradeManager.get_current_simulated_price(active_outcome)
            
            if simulated_price:
                entry_price = float(active_outcome.trade.price)
                current_price = float(simulated_price)
                change_from_entry = ((current_price - entry_price) / entry_price) * 100
                
                return Response({
                    'symbol': symbol,
                    'price': current_price,
                    'entry_price': entry_price,
                    'change_from_entry': change_from_entry,
                    'expected_outcome': active_outcome.outcome,
                    'expected_percentage': float(active_outcome.outcome_percentage),
                    'remaining_seconds': int((active_outcome.target_close_time - timezone.now()).total_seconds()),
                    'has_active_trade': True,
                    'timestamp': timezone.now().isoformat()
                })
        
        # No active trade - return current price from database
        try:
            crypto = Cryptocurrency.objects.get(symbol=symbol)
            return Response({
                'symbol': symbol,
                'price': float(crypto.current_price),
                'has_active_trade': False,
                'timestamp': timezone.now().isoformat()
            })
        except Cryptocurrency.DoesNotExist:
            return Response(
                {'error': f'Cryptocurrency {symbol} not found'},
                status=404
            )
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=500
        )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_real_price(request):
    """
    Get real cryptocurrency price from external APIs (CoinGecko/CCXT)
    
    Query params:
    - symbol: Cryptocurrency symbol (default: BTC)
    """
    try:
        symbol = request.query_params.get('symbol', 'BTC')
        
        # Check if real prices are enabled
        settings = TradingSettings.get_active_settings()
        if not settings.use_real_prices:
            return Response(
                {'error': 'Real prices are not enabled. Please enable in Trading Settings.'},
                status=400
            )
        
        # Get price service
        price_service = get_price_service()
        
        # Check if service is available
        if not price_service.is_available():
            return Response(
                {'error': 'Real price service is currently unavailable'},
                status=503
            )
        
        # Get current price
        price = price_service.get_current_price(symbol)
        
        if price is None:
            return Response(
                {'error': f'Unable to fetch price for {symbol}'},
                status=404
            )
        
        # Get 24h stats if available
        stats = price_service.get_24h_stats(symbol)
        
        return Response({
            'symbol': symbol,
            'price': price,
            'timestamp': timezone.now().isoformat(),
            'source': 'real',
            **stats
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=500
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_real_chart_data(request):
    """
    Get real historical chart data from external APIs
    
    Query params:
    - symbol: Cryptocurrency symbol (default: BTC)
    - interval: 'minutely' | 'hourly' | 'daily' (default: hourly)
    - days: Number of days of history (default: 1)
    """
    try:
        symbol = request.query_params.get('symbol', 'BTC')
        interval = request.query_params.get('interval', 'hourly')
        days = int(request.query_params.get('days', 1))
        
        # Check if real prices are enabled
        settings = TradingSettings.get_active_settings()
        if not settings.use_real_prices:
            return Response(
                {'error': 'Real prices are not enabled. Please enable in Trading Settings.'},
                status=400
            )
        
        # Get price service
        price_service = get_price_service()
        
        # Get historical data
        candles = price_service.get_historical_data(symbol, days=days, interval=interval)
        
        if not candles:
            return Response(
                {'error': f'Unable to fetch chart data for {symbol}'},
                status=404
            )
        
        # Get current price
        current_price = price_service.get_current_price(symbol)
        
        return Response({
            'symbol': symbol,
            'current_price': current_price,
            'interval': interval,
            'days': days,
            'chart_data': candles,
            'source': 'real',
            'count': len(candles)
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=500
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_price_auto(request):
    """
    Automatically get price based on settings (real or simulated)
    Respects the use_real_prices setting
    
    Query params:
    - symbol: Cryptocurrency symbol (default: BTC)
    """
    try:
        symbol = request.query_params.get('symbol', 'BTC')
        
        # Get settings
        settings = TradingSettings.get_active_settings()
        
        if settings.use_real_prices:
            # Use real prices
            price_service = get_price_service()
            
            if price_service.is_available():
                price = price_service.get_current_price(symbol)
                
                if price:
                    return Response({
                        'symbol': symbol,
                        'price': price,
                        'timestamp': timezone.now().isoformat(),
                        'source': 'real'
                    })
        
        # Fallback to database/simulated price
        try:
            crypto = Cryptocurrency.objects.get(symbol=symbol)
            return Response({
                'symbol': symbol,
                'price': float(crypto.current_price),
                'timestamp': timezone.now().isoformat(),
                'source': 'simulated'
            })
        except Cryptocurrency.DoesNotExist:
            return Response(
                {'error': f'Cryptocurrency {symbol} not found'},
                status=404
            )
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=500
        )
