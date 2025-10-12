from celery import shared_task
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def cleanup_old_chart_data():
    """
    Celery task to automatically clean up chart data older than 24 hours.
    This task should be run every hour to keep the database clean.
    """
    try:
        from market_data.models import ChartDataPoint
        
        # Clean up data older than 24 hours
        deleted_count = ChartDataPoint.cleanup_old_data(hours=24)
        
        logger.info(f"Cleaned up {deleted_count} old chart data points")
        
        return {
            'success': True,
            'deleted_count': deleted_count,
            'timestamp': timezone.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to cleanup old chart data: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }

@shared_task
def generate_initial_chart_data():
    """
    Generate initial chart data for popular cryptocurrencies.
    This task can be run to populate the database with initial data.
    """
    try:
        from market_data.models import ChartDataPoint
        from decimal import Decimal
        import random
        from datetime import timedelta
        
        symbols = ['BTC', 'ETH', 'SOL', 'XRP', 'ADA']
        current_time = timezone.now()
        
        for symbol in symbols:
            # Check if we already have data for this symbol
            if ChartDataPoint.objects.filter(symbol=symbol).exists():
                logger.info(f"Data already exists for {symbol}, skipping")
                continue
            
            # Generate 30 data points (1 hour of data at 2-minute intervals)
            base_price = Decimal('43250.50') if symbol == 'BTC' else Decimal('2650.75') if symbol == 'ETH' else Decimal('98.45')
            
            for i in range(30):
                timestamp = current_time - timedelta(minutes=i * 2)
                
                # Generate realistic price movement
                volatility = float(base_price) * 0.02
                open_price = base_price + Decimal(str((random.random() - 0.5) * volatility))
                close_price = open_price + Decimal(str((random.random() - 0.5) * volatility * 0.5))
                high_price = max(open_price, close_price) + Decimal(str(random.random() * volatility * 0.3))
                low_price = min(open_price, close_price) - Decimal(str(random.random() * volatility * 0.3))
                volume = Decimal(str(random.random() * 1000000))
                
                ChartDataPoint.objects.create(
                    symbol=symbol,
                    timestamp=timestamp,
                    open_price=open_price,
                    high_price=high_price,
                    low_price=low_price,
                    close_price=close_price,
                    volume=volume,
                    source='simulated'
                )
                
                base_price = close_price  # Use close price as next open price
            
            logger.info(f"Generated initial chart data for {symbol}")
        
        return {
            'success': True,
            'symbols_processed': symbols,
            'timestamp': timezone.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to generate initial chart data: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }
