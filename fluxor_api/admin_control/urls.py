"""
URL patterns for admin control.
"""
from django.urls import path
from . import views
from . import market_data_views
from . import chart_data_endpoints

app_name = 'admin_control'

urlpatterns = [
    # Trading settings
    path('settings/', views.TradingSettingsView.as_view(), name='trading_settings'),
    path('settings/win-loss/', views.update_win_loss_rates, name='update_win_loss'),
    path('settings/toggle/', views.toggle_biased_trading, name='toggle_biased'),
    path('settings/activity-based/', views.update_activity_based_settings, name='activity_based_settings'),
    path('settings/default/', views.set_default_settings, name='set_default_settings'),
    path('settings/mode-status/', views.get_trading_mode_status, name='trading_mode_status'),
    
    # Trade outcomes
    path('outcomes/', views.UserTradeOutcomeListView.as_view(), name='trade_outcomes'),
    path('outcomes/active/', views.get_active_positions_summary, name='active_positions'),
    
    # Market data
    path('market-history/', views.MarketDataHistoryView.as_view(), name='market_history'),
    path('market/live-chart/', market_data_views.get_live_chart_data, name='live_chart_data'),
    path('market/current-price/', market_data_views.get_current_price_update, name='current_price'),
    
    # Real price data
    path('market/real-price/', market_data_views.get_real_price, name='real_price'),
    path('market/real-chart/', market_data_views.get_real_chart_data, name='real_chart'),
    path('market/price-auto/', market_data_views.get_price_auto, name='price_auto'),
    
    # Chart data storage
    path('market/stored-chart/', chart_data_endpoints.get_stored_chart_data, name='stored_chart_data'),
    path('market/store-data-point/', chart_data_endpoints.store_chart_data_point, name='store_data_point'),
    path('market/combined-chart/', chart_data_endpoints.get_combined_chart_data, name='combined_chart_data'),
]
