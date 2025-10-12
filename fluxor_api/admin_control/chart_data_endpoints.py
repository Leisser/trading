"""
Additional endpoints for chart data storage and retrieval
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from trades.models import Cryptocurrency
from .models import TradingSettings
from .real_price_service import get_price_service
from market_data.models import ChartDataPoint
import random


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stored_chart_data(request):
    """
    Get chart data from database storage (ChartDataPoint model)
    
    Query params:
    - symbol: Cryptocurrency symbol (default: BTC)
    - limit: Number of data points (default: 30)
    """
    try:
        symbol = request.query_params.get('symbol', 'BTC')
        limit = int(request.query_params.get('limit', 30))
        
        # Get stored chart data from database
        chart_data = ChartDataPoint.get_latest_data(symbol, limit)
        
        if not chart_data:
            # If no data exists, return empty array
            return Response({
                'symbol': symbol,
                'chart_data': [],
                'count': 0,
                'source': 'stored',
                'message': 'No historical data available'
            })
        
        # Convert to frontend format
        formatted_data = []
        for point in reversed(chart_data):  # Reverse to get chronological order
            formatted_data.append({
                'timestamp': point.timestamp.isoformat(),
                'open': float(point.open_price),
                'high': float(point.high_price),
                'low': float(point.low_price),
                'close': float(point.close_price),
                'volume': float(point.volume)
            })
        
        return Response({
            'symbol': symbol,
            'chart_data': formatted_data,
            'count': len(formatted_data),
            'source': 'stored',
            'data_source': chart_data[0].source if chart_data else 'unknown'
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=500
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_chart_data_point(request):
    """
    Store a new chart data point in the database
    
    Body:
    - symbol: Cryptocurrency symbol (e.g., 'BTC')
    - timestamp: ISO timestamp string
    - open_price: Decimal price
    - high_price: Decimal price
    - low_price: Decimal price
    - close_price: Decimal price
    - volume: Decimal volume
    - source: 'real', 'simulated', or 'hybrid'
    """
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['symbol', 'timestamp', 'open_price', 'high_price', 'low_price', 'close_price']
        for field in required_fields:
            if field not in data:
                return Response(
                    {'error': f'Missing required field: {field}'},
                    status=400
                )
        
        # Parse timestamp
        from datetime import datetime
        if isinstance(data['timestamp'], str):
            timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
        else:
            timestamp = data['timestamp']
        
        # Create chart data point
        chart_point = ChartDataPoint.objects.create(
            symbol=data['symbol'],
            timestamp=timestamp,
            open_price=Decimal(str(data['open_price'])),
            high_price=Decimal(str(data['high_price'])),
            low_price=Decimal(str(data['low_price'])),
            close_price=Decimal(str(data['close_price'])),
            volume=Decimal(str(data.get('volume', 0))),
            source=data.get('source', 'simulated')
        )
        
        return Response({
            'message': 'Chart data point stored successfully',
            'id': chart_point.id,
            'timestamp': chart_point.timestamp.isoformat()
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=500
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_combined_chart_data(request):
    """
    Get combined chart data - stored historical data + live current price
    
    Query params:
    - symbol: Cryptocurrency symbol (default: BTC)
    - limit: Number of historical data points (default: 29, so total = 30 with current)
    - interval: Time interval ('seconds', 'minutes', 'hours') - default: 'seconds'
    """
    try:
        symbol = request.query_params.get('symbol', 'BTC')
        limit = int(request.query_params.get('limit', 29))  # 29 historical + 1 current = 30 total
        interval = request.query_params.get('interval', 'seconds')  # Default to seconds
        
        # Get stored historical data
        stored_data = ChartDataPoint.get_latest_data(symbol, limit)
        
        # Get current price (auto-switches between real/simulated)
        settings = TradingSettings.get_active_settings()
        current_price_data = None
        
        if settings.use_real_prices:
            # Try to get real price
            price_service = get_price_service()
            if price_service.is_available():
                current_price = price_service.get_current_price(symbol)
                if current_price:
                    current_price_data = {
                        'price': current_price,
                        'source': 'real'
                    }
        
        # Fallback to simulated price
        if not current_price_data:
            try:
                crypto = Cryptocurrency.objects.get(symbol=symbol)
                current_price_data = {
                    'price': float(crypto.current_price),
                    'source': 'simulated'
                }
            except Cryptocurrency.DoesNotExist:
                current_price_data = {
                    'price': 43250.50,  # Default BTC price
                    'source': 'simulated'
                }
        
        # Generate data with correct intervals (always respect interval parameter)
        # If interval is 'seconds' (default), use stored data if available
        # If interval is 'minutes' or 'hours', generate new data with proper spacing
        if interval == 'seconds' and len(stored_data) >= limit:
            # Use stored data for seconds interval (default behavior)
            formatted_data = []
            for point in reversed(stored_data):  # Chronological order
                formatted_data.append({
                    'timestamp': point.timestamp.isoformat(),
                    'open': float(point.open_price),
                    'high': float(point.high_price),
                    'low': float(point.low_price),
                    'close': float(point.close_price),
                    'volume': float(point.volume)
                })
            
            # Add current price as newest data point
            current_time = timezone.now()
            if formatted_data:
                last_close = formatted_data[-1]['close']
                current_open = last_close
            else:
                current_open = current_price_data['price']
            
            current_candle = {
                'timestamp': current_time.isoformat(),
                'open': current_open,
                'high': max(current_open, current_price_data['price']) * 1.003,
                'low': min(current_open, current_price_data['price']) * 0.997,
                'close': current_price_data['price'],
                'volume': 500000
            }
            
            formatted_data.append(current_candle)
        else:
            # Generate new data with correct intervals for minutes/hours or when no stored data
            formatted_data = generate_interval_data(symbol, limit, interval, current_price_data['price'])
        
        return Response({
            'symbol': symbol,
            'chart_data': formatted_data,
            'count': len(formatted_data),
            'current_price': current_price_data['price'],
            'source': 'combined',
            'price_source': current_price_data['source'],
            'has_stored_data': len(stored_data) > 0,
            'interval': interval,
            'time_range': f"{limit} {interval}"
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=500
        )


def generate_interval_data(symbol, limit, interval, current_price):
    """
    Generate chart data with correct time intervals
    
    Args:
        symbol: Cryptocurrency symbol
        limit: Number of data points to generate
        interval: 'seconds', 'minutes', or 'hours'
        current_price: Current price to use as base
    
    Returns:
        List of formatted chart data points
    """
    formatted_data = []
    base_price = current_price
    current_time = timezone.now()
    
    # Determine time increment based on interval
    if interval == 'seconds':
        time_increment = 2  # 2 seconds between points
    elif interval == 'minutes':
        time_increment = 1  # 1 minute between points
    elif interval == 'hours':
        time_increment = 1  # 1 hour between points
    else:
        time_increment = 2  # Default to 2 seconds
    
    for i in range(limit):
        # Calculate timestamp
        if interval == 'seconds':
            timestamp = current_time - timedelta(seconds=i * time_increment)
        elif interval == 'minutes':
            timestamp = current_time - timedelta(minutes=i * time_increment)
        elif interval == 'hours':
            timestamp = current_time - timedelta(hours=i * time_increment)
        else:
            timestamp = current_time - timedelta(seconds=i * time_increment)
        
        # Generate realistic price movement
        volatility = float(base_price) * 0.02
        open_price = base_price + (random.random() - 0.5) * volatility
        close_price = open_price + (random.random() - 0.5) * volatility * 0.5
        high_price = max(open_price, close_price) + random.random() * volatility * 0.3
        low_price = min(open_price, close_price) - random.random() * volatility * 0.3
        volume = random.random() * 1000000
        
        formatted_data.append({
            'timestamp': timestamp.isoformat(),
            'open': float(open_price),
            'high': float(high_price),
            'low': float(low_price),
            'close': float(close_price),
            'volume': float(volume)
        })
        
        base_price = close_price  # Use close price as next open price
    
    # Reverse to get chronological order (oldest first)
    formatted_data.reverse()
    
    # Add current price as the newest data point
    current_candle = {
        'timestamp': current_time.isoformat(),
        'open': float(base_price),
        'high': max(base_price, current_price) * 1.003,
        'low': min(base_price, current_price) * 0.997,
        'close': float(current_price),
        'volume': 500000
    }
    
    formatted_data.append(current_candle)
    
    return formatted_data
