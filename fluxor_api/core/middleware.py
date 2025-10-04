import time
import json
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

class RateLimitMiddleware:
    """Middleware for API rate limiting"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limits = {
            'default': {'requests': 100, 'window': 60},  # 100 requests per minute
            'auth': {'requests': 5, 'window': 60},       # 5 auth attempts per minute
            'trading': {'requests': 50, 'window': 60},   # 50 trading requests per minute
            'data': {'requests': 200, 'window': 60},     # 200 data requests per minute
        }
    
    def __call__(self, request):
        # Skip rate limiting for admin and static files
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return self.get_response(request)
        
        # Get client identifier
        client_id = self.get_client_id(request)
        
        # Determine rate limit type based on path
        rate_limit_type = self.get_rate_limit_type(request.path)
        
        # Check rate limit
        if not self.check_rate_limit(client_id, rate_limit_type):
            return JsonResponse({
                'error': 'Rate limit exceeded',
                'message': f'Too many requests. Limit: {self.rate_limits[rate_limit_type]["requests"]} requests per {self.rate_limits[rate_limit_type]["window"]} seconds'
            }, status=429)
        
        response = self.get_response(request)
        return response
    
    def get_client_id(self, request):
        """Get unique client identifier"""
        # Use IP address as primary identifier
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Add user ID if authenticated
        if hasattr(request, 'user') and request.user.is_authenticated:
            return f"{ip}:{request.user.id}"
        
        return ip
    
    def get_rate_limit_type(self, path):
        """Determine rate limit type based on request path"""
        if path.startswith('/api/auth/'):
            return 'auth'
        elif path.startswith('/api/trading/') or path.startswith('/api/orders/'):
            return 'trading'
        elif path.startswith('/api/market-data/') or path.startswith('/api/price/'):
            return 'data'
        else:
            return 'default'
    
    def check_rate_limit(self, client_id, rate_limit_type):
        """Check if request is within rate limit"""
        limit_config = self.rate_limits[rate_limit_type]
        window = limit_config['window']
        max_requests = limit_config['requests']
        
        # Create cache key
        cache_key = f"rate_limit:{client_id}:{rate_limit_type}"
        
        # Get current requests count
        current_requests = cache.get(cache_key, 0)
        
        if current_requests >= max_requests:
            return False
        
        # Increment request count
        cache.set(cache_key, current_requests + 1, window)
        return True

class RequestLoggingMiddleware:
    """Middleware for logging API requests"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Log request start time
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Calculate request duration
        duration = time.time() - start_time
        
        # Log request details
        self.log_request(request, response, duration)
        
        return response
    
    def log_request(self, request, response, duration):
        """Log request details"""
        import logging
        logger = logging.getLogger('api_requests')
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Get user info
        user_id = None
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_id = request.user.id
        
        # Log request
        log_data = {
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration': round(duration, 3),
            'ip': ip,
            'user_id': user_id,
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }
        
        # Log based on status code
        if response.status_code >= 400:
            logger.warning(f"API Request: {log_data}")
        else:
            logger.info(f"API Request: {log_data}")

class SecurityMiddleware:
    """Middleware for security headers and checks"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response 