from django.urls import path
from .views import (
    PriceFeedView, TradingSignalView, ExecuteTradeView, OrderBookView,
    MarketDataView, TradingStrategyView
)

app_name = 'trading_engine'

urlpatterns = [
    # Price and market data
    path('price_feed/', PriceFeedView.as_view(), name='price_feed'),
    path('market_data/', MarketDataView.as_view(), name='market_data'),
    path('order_book/', OrderBookView.as_view(), name='order_book'),
    
    # Trading signals and execution
    path('trading_signal/', TradingSignalView.as_view(), name='trading_signal'),
    path('execute_trade/', ExecuteTradeView.as_view(), name='execute_trade'),
    
    # Strategy management
    path('strategies/', TradingStrategyView.as_view(), name='trading_strategies'),
] 