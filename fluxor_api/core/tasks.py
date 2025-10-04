import logging
from datetime import datetime, timedelta
from celery import shared_task
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)

@shared_task
def cleanup_old_data():
    """Clean up old data to maintain database performance"""
    try:
        from market_data.models import MarketData, Ticker, OrderBook, Trade
        from trades.models import Trade as UserTrade
        from blockchain.models import Transaction, MempoolTransaction
        
        # Calculate cutoff dates
        market_data_cutoff = timezone.now() - timedelta(days=30)
        trade_cutoff = timezone.now() - timedelta(days=90)
        mempool_cutoff = timezone.now() - timedelta(hours=24)
        
        # Clean up old market data
        deleted_market_data = MarketData.objects.filter(
            timestamp__lt=market_data_cutoff
        ).delete()
        
        # Clean up old tickers
        deleted_tickers = Ticker.objects.filter(
            timestamp__lt=market_data_cutoff
        ).delete()
        
        # Clean up old order books
        deleted_orderbooks = OrderBook.objects.filter(
            timestamp__lt=market_data_cutoff
        ).delete()
        
        # Clean up old trades
        deleted_trades = Trade.objects.filter(
            timestamp__lt=market_data_cutoff
        ).delete()
        
        # Clean up old user trades (keep longer for compliance)
        deleted_user_trades = UserTrade.objects.filter(
            created_at__lt=trade_cutoff
        ).delete()
        
        # Clean up old mempool transactions
        deleted_mempool = MempoolTransaction.objects.filter(
            created_at__lt=mempool_cutoff
        ).delete()
        
        logger.info(f"Cleanup completed: {deleted_market_data[0]} market data, "
                   f"{deleted_tickers[0]} tickers, {deleted_orderbooks[0]} order books, "
                   f"{deleted_trades[0]} trades, {deleted_user_trades[0]} user trades, "
                   f"{deleted_mempool[0]} mempool transactions")
        
        return {
            'market_data_deleted': deleted_market_data[0],
            'tickers_deleted': deleted_tickers[0],
            'orderbooks_deleted': deleted_orderbooks[0],
            'trades_deleted': deleted_trades[0],
            'user_trades_deleted': deleted_user_trades[0],
            'mempool_deleted': deleted_mempool[0],
        }
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        raise

@shared_task
def clear_expired_cache():
    """Clear expired cache entries"""
    try:
        # Clear rate limiting cache
        cache.delete_pattern("rate_limit:*")
        
        # Clear other temporary cache entries
        cache.delete_pattern("temp_*")
        cache.delete_pattern("session_*")
        
        logger.info("Cache cleanup completed")
        return True
        
    except Exception as e:
        logger.error(f"Error during cache cleanup: {str(e)}")
        raise

@shared_task
def health_check():
    """Perform system health check"""
    try:
        from django.db import connection
        from django.core.cache import cache
        
        health_status = {
            'database': False,
            'cache': False,
            'timestamp': timezone.now().isoformat(),
        }
        
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                health_status['database'] = True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
        
        # Check cache connection
        try:
            cache.set('health_check', 'ok', 10)
            if cache.get('health_check') == 'ok':
                health_status['cache'] = True
        except Exception as e:
            logger.error(f"Cache health check failed: {str(e)}")
        
        logger.info(f"Health check completed: {health_status}")
        return health_status
        
    except Exception as e:
        logger.error(f"Error during health check: {str(e)}")
        raise

@shared_task
def backup_database():
    """Create database backup"""
    try:
        import subprocess
        from django.conf import settings
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_{timestamp}.sql"
        backup_path = f"backups/{backup_filename}"
        
        # Create backups directory if it doesn't exist
        import os
        os.makedirs("backups", exist_ok=True)
        
        # Get database settings
        db_settings = settings.DATABASES['default']
        
        # Create backup command
        if db_settings['ENGINE'] == 'django.db.backends.postgresql':
            cmd = [
                'pg_dump',
                '-h', db_settings['HOST'],
                '-p', str(db_settings['PORT']),
                '-U', db_settings['USER'],
                '-d', db_settings['NAME'],
                '-f', backup_path
            ]
            
            # Set password environment variable
            env = os.environ.copy()
            env['PGPASSWORD'] = db_settings['PASSWORD']
            
            # Execute backup
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Database backup created: {backup_path}")
                return {'status': 'success', 'file': backup_path}
            else:
                logger.error(f"Database backup failed: {result.stderr}")
                return {'status': 'error', 'message': result.stderr}
        
        else:
            logger.warning("Backup not implemented for this database engine")
            return {'status': 'not_implemented'}
            
    except Exception as e:
        logger.error(f"Error during database backup: {str(e)}")
        raise

@shared_task
def monitor_system_resources():
    """Monitor system resources"""
    try:
        import psutil
        
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available': memory.available,
            'disk_percent': disk.percent,
            'disk_free': disk.free,
            'timestamp': timezone.now().isoformat(),
        }
        
        # Log warning if resources are high
        if cpu_percent > 80:
            logger.warning(f"High CPU usage: {cpu_percent}%")
        
        if memory.percent > 80:
            logger.warning(f"High memory usage: {memory.percent}%")
        
        if disk.percent > 90:
            logger.warning(f"High disk usage: {disk.percent}%")
        
        # Store metrics in cache for monitoring
        cache.set('system_metrics', metrics, 300)  # 5 minutes
        
        return metrics
        
    except ImportError:
        logger.warning("psutil not installed, skipping system monitoring")
        return {'status': 'psutil_not_installed'}
    except Exception as e:
        logger.error(f"Error during system monitoring: {str(e)}")
        raise 