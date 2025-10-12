"""
WebSocket URL routing for Fluxor API.
"""

from django.urls import path
from . import consumers
from .market_consumer import MarketDataConsumer as LiveMarketConsumer
from trades.consumers import TradeUpdateConsumer

websocket_urlpatterns = [
    path('ws/trading/', consumers.TradingConsumer.as_asgi()),
    path('ws/market/', consumers.MarketDataConsumer.as_asgi()),
    path('ws/market/<str:symbol>/', LiveMarketConsumer.as_asgi()),  # Live market data with symbol
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
    path('ws/trades/', TradeUpdateConsumer.as_asgi()),  # Real-time trade updates
]
