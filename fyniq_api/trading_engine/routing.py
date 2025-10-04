from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/price_feed/$', consumers.PriceFeedConsumer.as_asgi()),
    re_path(r'ws/trade_updates/$', consumers.TradeUpdateConsumer.as_asgi()),
] 