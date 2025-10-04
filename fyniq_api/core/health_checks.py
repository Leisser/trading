"""
Health Check System for Fluxor Trading API
Monitors all critical components and dependencies
"""

import time
import psutil
from django.db import connection
from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import redis
import ccxt
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class HealthCheckService:
    """Comprehensive health check service"""
    
    def __init__(self):
        self.checks = {
            'database': self.check_database,
            'redis': self.check_redis,
            'celery': self.check_celery,
            'exchanges': self.check_exchanges,
            'disk_space': self.check_disk_space,
            'memory': self.check_memory,
            'websockets': self.check_websockets,
        }
    
    def run_all_checks(self):
        """Run all health checks"""
        results = {}
        overall_status = 'healthy'
        
        for check_name, check_func in self.checks.items():
            try:
                start_time = time.time()
                result = check_func()
                duration = time.time() - start_time
                
                results[check_name] = {
                    'status': result.get('status', 'unknown'),
                    'message': result.get('message', ''),
                    'details': result.get('details', {}),
                    'response_time': round(duration, 3)
                }
                
                if result.get('status') != 'healthy':
                    overall_status = 'unhealthy'
                    
            except Exception as e:
                logger.error(f"Health check failed for {check_name}: {str(e)}")
                results[check_name] = {
                    'status': 'error',
                    'message': str(e),
                    'details': {},
                    'response_time': 0
                }
                overall_status = 'unhealthy'
        
        return {
            'status': overall_status,
            'timestamp': time.time(),
            'checks': results,
            'version': getattr(settings, 'VERSION', '1.0.0'),
            'uptime': self.get_uptime()
        }
    
    def check_database(self):
        """Check database connectivity and performance"""
        try:
            start_time = time.time()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            query_time = time.time() - start_time
            
            # Check connection pool
            db_connections = len(connection.queries) if settings.DEBUG else 0
            
            return {
                'status': 'healthy',
                'message': 'Database connection successful',
                'details': {
                    'query_time': round(query_time, 3),
                    'active_connections': db_connections,
                    'database': settings.DATABASES['default']['NAME']
                }
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Database connection failed: {str(e)}',
                'details': {}
            }
    
    def check_redis(self):
        """Check Redis connectivity and performance"""
        try:
            start_time = time.time()
            
            # Test cache
            test_key = 'health_check_test'
            cache.set(test_key, 'test_value', 10)
            value = cache.get(test_key)
            cache.delete(test_key)
            
            if value != 'test_value':
                raise Exception("Cache read/write test failed")
            
            cache_time = time.time() - start_time
            
            # Get Redis info
            redis_client = redis.from_url(settings.REDIS_URL)
            redis_info = redis_client.info()
            
            return {
                'status': 'healthy',
                'message': 'Redis connection successful',
                'details': {
                    'cache_time': round(cache_time, 3),
                    'used_memory': redis_info.get('used_memory_human'),
                    'connected_clients': redis_info.get('connected_clients'),
                    'version': redis_info.get('redis_version')
                }
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Redis connection failed: {str(e)}',
                'details': {}
            }
    
    def check_celery(self):
        """Check Celery worker and beat status"""
        try:
            from celery import current_app
            
            # Check if workers are active
            inspect = current_app.control.inspect()
            stats = inspect.stats()
            
            if not stats:
                return {
                    'status': 'unhealthy',
                    'message': 'No Celery workers found',
                    'details': {}
                }
            
            active_workers = len(stats)
            
            # Check scheduled tasks
            scheduled = inspect.scheduled()
            active_tasks = inspect.active()
            
            return {
                'status': 'healthy',
                'message': f'{active_workers} Celery workers active',
                'details': {
                    'active_workers': active_workers,
                    'scheduled_tasks': len(scheduled) if scheduled else 0,
                    'active_tasks': len(active_tasks) if active_tasks else 0
                }
            }
        except Exception as e:
            return {
                'status': 'warning',
                'message': f'Celery check failed: {str(e)}',
                'details': {}
            }
    
    def check_exchanges(self):
        """Check cryptocurrency exchange connectivity"""
        exchange_status = {}
        
        try:
            # Test Binance connection
            binance = ccxt.binance({
                'apiKey': getattr(settings, 'BINANCE_API_KEY', ''),
                'secret': getattr(settings, 'BINANCE_SECRET_KEY', ''),
                'sandbox': getattr(settings, 'BINANCE_TESTNET', True),
                'enableRateLimit': True,
            })
            
            start_time = time.time()
            ticker = binance.fetch_ticker('BTC/USDT')
            response_time = time.time() - start_time
            
            exchange_status['binance'] = {
                'status': 'healthy',
                'response_time': round(response_time, 3),
                'btc_price': ticker['last']
            }
            
        except Exception as e:
            exchange_status['binance'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
        
        overall_status = 'healthy' if all(
            ex['status'] == 'healthy' for ex in exchange_status.values()
        ) else 'warning'
        
        return {
            'status': overall_status,
            'message': f'Exchange connectivity: {len(exchange_status)} exchanges checked',
            'details': exchange_status
        }
    
    def check_disk_space(self):
        """Check disk space usage"""
        try:
            disk_usage = psutil.disk_usage('/')
            
            # Convert to GB
            total_gb = disk_usage.total / (1024**3)
            used_gb = disk_usage.used / (1024**3)
            free_gb = disk_usage.free / (1024**3)
            usage_percent = (used_gb / total_gb) * 100
            
            status = 'healthy'
            if usage_percent > 90:
                status = 'critical'
            elif usage_percent > 80:
                status = 'warning'
            
            return {
                'status': status,
                'message': f'Disk usage: {usage_percent:.1f}%',
                'details': {
                    'total_gb': round(total_gb, 2),
                    'used_gb': round(used_gb, 2),
                    'free_gb': round(free_gb, 2),
                    'usage_percent': round(usage_percent, 2)
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Disk check failed: {str(e)}',
                'details': {}
            }
    
    def check_memory(self):
        """Check memory usage"""
        try:
            memory = psutil.virtual_memory()
            
            # Convert to MB
            total_mb = memory.total / (1024**2)
            used_mb = memory.used / (1024**2)
            available_mb = memory.available / (1024**2)
            usage_percent = memory.percent
            
            status = 'healthy'
            if usage_percent > 90:
                status = 'critical'
            elif usage_percent > 80:
                status = 'warning'
            
            return {
                'status': status,
                'message': f'Memory usage: {usage_percent:.1f}%',
                'details': {
                    'total_mb': round(total_mb, 2),
                    'used_mb': round(used_mb, 2),
                    'available_mb': round(available_mb, 2),
                    'usage_percent': usage_percent
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Memory check failed: {str(e)}',
                'details': {}
            }
    
    def check_websockets(self):
        """Check WebSocket functionality"""
        try:
            # This is a simplified check - in reality, you'd test actual WS connections
            from channels.layers import get_channel_layer
            
            channel_layer = get_channel_layer()
            
            if channel_layer is None:
                return {
                    'status': 'unhealthy',
                    'message': 'Channel layer not configured',
                    'details': {}
                }
            
            return {
                'status': 'healthy',
                'message': 'WebSocket layer configured',
                'details': {
                    'backend': str(type(channel_layer).__name__)
                }
            }
        except Exception as e:
            return {
                'status': 'warning',
                'message': f'WebSocket check failed: {str(e)}',
                'details': {}
            }
    
    def get_uptime(self):
        """Get system uptime"""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            
            return f"{days}d {hours}h {minutes}m"
        except:
            return "unknown"


# Django Views
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Basic health check endpoint"""
    health_service = HealthCheckService()
    result = health_service.run_all_checks()
    
    status_code = status.HTTP_200_OK if result['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return Response(result, status=status_code)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_simple(request):
    """Simple health check for load balancers"""
    try:
        # Quick database check
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'status': 'error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_detailed(request):
    """Detailed health check with all components"""
    health_service = HealthCheckService()
    result = health_service.run_all_checks()
    
    # Add additional system information
    result['system_info'] = {
        'python_version': psutil.python_version(),
        'platform': psutil.platform.platform(),
        'cpu_count': psutil.cpu_count(),
        'cpu_percent': psutil.cpu_percent(),
        'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
    }
    
    status_code = status.HTTP_200_OK if result['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return Response(result, status=status_code)


class TradingHealthCheck:
    """Trading-specific health checks"""
    
    @staticmethod
    def check_trading_system():
        """Check trading system health"""
        from risk_management.services import RiskManagementService
        from compliance.services import ComplianceService
        
        checks = {}
        
        try:
            # Test risk management
            risk_service = RiskManagementService()
            risk_check = risk_service.check_position_size(Decimal('1000'))
            checks['risk_management'] = {
                'status': 'healthy' if risk_check else 'warning',
                'message': 'Risk management system operational'
            }
        except Exception as e:
            checks['risk_management'] = {
                'status': 'error',
                'message': str(e)
            }
        
        try:
            # Test compliance
            compliance_service = ComplianceService()
            kyc_check = compliance_service.is_kyc_required(Decimal('500'))
            checks['compliance'] = {
                'status': 'healthy',
                'message': 'Compliance system operational'
            }
        except Exception as e:
            checks['compliance'] = {
                'status': 'error',
                'message': str(e)
            }
        
        return checks


@api_view(['GET'])
@permission_classes([AllowAny])
def trading_health_check(request):
    """Trading system specific health check"""
    trading_checks = TradingHealthCheck.check_trading_system()
    
    overall_status = 'healthy' if all(
        check['status'] == 'healthy' for check in trading_checks.values()
    ) else 'unhealthy'
    
    result = {
        'status': overall_status,
        'timestamp': time.time(),
        'trading_systems': trading_checks
    }
    
    status_code = status.HTTP_200_OK if overall_status == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return Response(result, status=status_code)