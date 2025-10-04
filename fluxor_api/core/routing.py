"""
WebSocket URL routing for Fluxor API.
"""

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/trading/', consumers.TradingConsumer.as_asgi()),
    path('ws/market/', consumers.MarketDataConsumer.as_asgi()),
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]
