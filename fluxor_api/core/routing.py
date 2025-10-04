from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/price/$', consumers.PriceConsumer.as_asgi()),
    re_path(r'ws/trading/$', consumers.TradingConsumer.as_asgi()),
    re_path(r'ws/alerts/$', consumers.AlertConsumer.as_asgi()),
    re_path(r'ws/market-data/$', consumers.MarketDataConsumer.as_asgi()),
] 