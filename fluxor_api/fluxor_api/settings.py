"""
Django settings for fluxor_api project.
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'channels',
    'drf_yasg',
    'accounts',
    'wallets',
    'trades',
    'blockchain',
    'core',
    'trading_engine',
    'risk_management',
    'compliance',
    'market_data',
    'order_management',
    'portfolio_management',
    'alerts',
    'reports',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'core.middleware.RateLimitMiddleware',
    'core.middleware.RequestLoggingMiddleware',
    'core.middleware.SecurityMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fluxor_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fluxor_api.wsgi.application'

# Channels Configuration for WebSocket
ASGI_APPLICATION = 'fluxor_api.asgi.application'

# Channel Layers for WebSocket
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [config('REDIS_URL', default='redis://localhost:6379/0')],
        },
    },
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='fluxor_api'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Settings - Enhanced for persistent Firebase sessions
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),  # 24 hours for better UX
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),  # 30 days for persistent sessions
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,  # Update last login on token refresh
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=24),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=30),
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Celery Configuration
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Bitcoin Configuration
BITCOIN_NETWORK = config('BITCOIN_NETWORK', default='testnet')  # 'mainnet' or 'testnet'
COMPANY_WALLET_LABEL = config('COMPANY_WALLET_LABEL', default='company_wallet')

# Trading Configuration
TRADING_CONFIG = {
    'DEFAULT_EXCHANGE': 'binance',
    'PRICE_UPDATE_INTERVAL': 5,  # seconds
    'RISK_CHECK_INTERVAL': 30,   # seconds
    'MAX_LEVERAGE': 10,
    'MAX_POSITION_SIZE': 10000,  # USD
    'STOP_LOSS_PERCENTAGE': 5,   # 5%
    'TAKE_PROFIT_PERCENTAGE': 10, # 10%
}

# Risk Management Configuration
RISK_CONFIG = {
    'MAX_DAILY_LOSS': 1000,      # USD
    'MAX_DAILY_VOLUME': 50000,   # USD
    'MAX_OPEN_POSITIONS': 5,
    'MIN_MARGIN_REQUIREMENT': 0.1, # 10%
    'LIQUIDATION_THRESHOLD': 0.05, # 5%
}

# Compliance Configuration
COMPLIANCE_CONFIG = {
    'KYC_REQUIRED_AMOUNT': 1000,  # USD
    'SUSPICIOUS_AMOUNT': 10000,   # USD
    'REPORTING_THRESHOLD': 5000,  # USD
    'AML_CHECK_INTERVAL': 3600,   # 1 hour
}

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}

# Create logs directory if it doesn't exist
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

# Enhanced settings from fluxor_backend
# Crypto and Blockchain settings
CRYPTO_ENCRYPTION_KEY = config('CRYPTO_ENCRYPTION_KEY', default='HvTbFJudn1UHkClQamG6j3KA6IZVCZRnSySBtltlbFo=')
ETHEREUM_RPC_URL = config('ETHEREUM_RPC_URL', default='https://mainnet.infura.io/v3/your-project-id')

# CoinGecko API settings
COINGECKO_API_KEY = config('COINGECKO_API_KEY', default='')  # Optional for higher rate limits

# Coinbase Commerce settings
COINBASE_COMMERCE_API_KEY = config('COINBASE_COMMERCE_API_KEY', default='')
COINBASE_COMMERCE_WEBHOOK_SECRET = config('COINBASE_COMMERCE_WEBHOOK_SECRET', default='')

# NOWPayments settings
NOWPAYMENTS_API_KEY = config('NOWPAYMENTS_API_KEY', default='')
NOWPAYMENTS_IPN_SECRET = config('NOWPAYMENTS_IPN_SECRET', default='')

# 1inch API settings for swaps
INCH_API_KEY = config('INCH_API_KEY', default='')

# Binance API settings
BINANCE_API_KEY = config('BINANCE_API_KEY', default='')
BINANCE_SECRET_KEY = config('BINANCE_SECRET_KEY', default='')

# Crypto payment providers
CRYPTO_PAYMENT_PROVIDERS = {
    'coinbase': {
        'enabled': True,
        'api_key': COINBASE_COMMERCE_API_KEY,
        'webhook_secret': COINBASE_COMMERCE_WEBHOOK_SECRET,
    },
    'nowpayments': {
        'enabled': True,
        'api_key': NOWPAYMENTS_API_KEY,
        'ipn_secret': NOWPAYMENTS_IPN_SECRET,
    },
    'bitpay': {
        'enabled': False,
        'api_key': config('BITPAY_API_KEY', default=''),
    },
    'btcpay': {
        'enabled': False,
        'server_url': config('BTCPAY_SERVER_URL', default=''),
        'api_key': config('BTCPAY_API_KEY', default=''),
    },
}

# Supported cryptocurrencies
SUPPORTED_CRYPTOCURRENCIES = [
    {'symbol': 'BTC', 'name': 'Bitcoin', 'wallet_type': 'bitcoin'},
    {'symbol': 'ETH', 'name': 'Ethereum', 'wallet_type': 'ethereum'},
    {'symbol': 'SOL', 'name': 'Solana', 'wallet_type': 'solana'},
    {'symbol': 'ADA', 'name': 'Cardano', 'wallet_type': 'cardano'},
    {'symbol': 'DOT', 'name': 'Polkadot', 'wallet_type': 'polkadot'},
    {'symbol': 'LINK', 'name': 'Chainlink', 'wallet_type': 'chainlink'},
]

# Swap providers
SWAP_PROVIDERS = {
    '1inch': {
        'enabled': True,
        'api_key': INCH_API_KEY,
        'base_url': 'https://api.1inch.dev',
    },
    'uniswap': {
        'enabled': False,
        'api_key': config('UNISWAP_API_KEY', default=''),
    },
}

# Price update settings
PRICE_UPDATE_INTERVAL = 30  # seconds
PRICE_SOURCES = ['coingecko', 'binance']

# Security settings for crypto operations
CRYPTO_SECURITY = {
    'max_transaction_amount': 10000,  # USD
    'min_transaction_amount': 1,      # USD
    'daily_transaction_limit': 50000, # USD
    'require_2fa_for_large_transactions': True,
    'large_transaction_threshold': 1000,  # USD
} 