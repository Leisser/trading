"""
URL patterns for Market Data API.
"""
from django.urls import path
from .views import (
    RealTimePriceView, OHLCVDataView, OrderBookView, TradingPairsView,
    PriceAlertListView, PriceAlertDetailView, TechnicalAnalysisView,
    sync_market_data, get_cryptocurrencies
)

app_name = 'market_data'

urlpatterns = [
    # Real-time data
    path('price/', RealTimePriceView.as_view(), name='real_time_price'),
    path('ohlcv/', OHLCVDataView.as_view(), name='ohlcv_data'),
    path('orderbook/', OrderBookView.as_view(), name='order_book'),
    path('pairs/', TradingPairsView.as_view(), name='trading_pairs'),
    
    # Technical analysis
    path('technical/', TechnicalAnalysisView.as_view(), name='technical_analysis'),
    
    # Price alerts
    path('alerts/', PriceAlertListView.as_view(), name='price_alerts'),
    path('alerts/<int:pk>/', PriceAlertDetailView.as_view(), name='price_alert_detail'),
    
    # Data sync
    path('sync/', sync_market_data, name='sync_market_data'),
    
    # Dashboard endpoints
    path('cryptocurrencies/', get_cryptocurrencies, name='cryptocurrencies'),
]
