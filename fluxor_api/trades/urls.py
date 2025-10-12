"""
URL patterns for trades app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets (if any)
router = DefaultRouter()

app_name = 'trades'

urlpatterns = [
    # Cryptocurrency endpoints
    path('cryptocurrencies/', views.CryptocurrencyListView.as_view(), name='cryptocurrency_list'),
    path('cryptocurrencies/<str:symbol>/', views.CryptocurrencyDetailView.as_view(), name='cryptocurrency_detail'),
    path('cryptocurrencies/create/', views.CryptocurrencyCreateView.as_view(), name='cryptocurrency_create'),
    path('cryptocurrencies/<str:symbol>/update/', views.CryptocurrencyUpdateView.as_view(), name='cryptocurrency_update'),
    path('cryptocurrencies/<str:symbol>/delete/', views.CryptocurrencyDeleteView.as_view(), name='cryptocurrency_delete'),
    
    # Cryptocurrency utility endpoints
    path('cryptocurrencies/top/', views.get_top_cryptocurrencies, name='top_cryptocurrencies'),
    path('cryptocurrencies/featured/', views.get_featured_cryptocurrencies, name='featured_cryptocurrencies'),
    path('cryptocurrencies/stablecoins/', views.get_stablecoins, name='stablecoins'),
    path('cryptocurrencies/categories/', views.get_cryptocurrency_categories, name='cryptocurrency_categories'),
    path('cryptocurrencies/search/', views.search_cryptocurrencies, name='search_cryptocurrencies'),
    path('cryptocurrencies/stats/', views.get_cryptocurrency_stats, name='cryptocurrency_stats'),
    
    # Crypto wallet endpoints
    path('wallets/', views.CryptoWalletListView.as_view(), name='crypto_wallet_list'),
    path('wallets/<int:pk>/', views.CryptoWalletDetailView.as_view(), name='crypto_wallet_detail'),
    
    # Trading endpoints
    path('trades/', views.TradeListView.as_view(), name='trade_list'),
    path('trades/<int:pk>/', views.TradeDetailView.as_view(), name='trade_detail'),
    
    # Deposit and withdrawal endpoints
    path('deposits/', views.DepositListView.as_view(), name='deposit_list'),
    path('withdrawals/', views.WithdrawalListView.as_view(), name='withdrawal_list'),
    
    # Crypto index endpoints
    path('indices/', views.CryptoIndexListView.as_view(), name='crypto_index_list'),
    path('indices/<str:symbol>/', views.CryptoIndexDetailView.as_view(), name='crypto_index_detail'),
    
    # Investment endpoints
    path('investments/', views.CryptoInvestmentListView.as_view(), name='crypto_investment_list'),
    path('investments/<int:pk>/', views.CryptoInvestmentDetailView.as_view(), name='crypto_investment_detail'),

    # Dashboard stats
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),

    # Admin users list
    path('admin/users/', views.admin_users_list, name='admin_users_list'),

    # Admin endpoints for wallet management
    path('admin/deposits/', views.AdminDepositRequestListView.as_view(), name='admin_deposit_list'),
    path('admin/deposits/<int:deposit_id>/approve/', views.AdminDepositApprovalView.as_view(), name='admin_deposit_approve'),
    path('admin/withdrawals/', views.AdminWithdrawalRequestListView.as_view(), name='admin_withdrawal_list'),
    path('admin/withdrawals/<int:withdrawal_id>/approve/', views.AdminWithdrawalApprovalView.as_view(), name='admin_withdrawal_approve'),

    # Trading endpoints
    path('trading/pairs/', views.TradingPairListView.as_view(), name='trading_pairs'),
    path('trading/orderbook/<str:pair_id>/', views.OrderBookView.as_view(), name='order_book'),
    path('trading/orders/', views.PlaceOrderView.as_view(), name='place_order'),
    path('trading/orders/user/', views.UserOrdersView.as_view(), name='user_orders'),

    # New trade execution endpoints with balance validation
    path('trading/execute/', views.execute_trade, name='execute_trade'),
    path('trading/balance/check/', views.check_balance, name='check_balance'),
    path('trading/history/', views.get_trading_history, name='trading_history'),
    path('trading/deduct-balance/', views.DeductBalanceView.as_view(), name='deduct_balance'),
    path('trading/stop/<int:trade_id>/', views.StopTradeView.as_view(), name='stop_trade'),

    # Include router URLs
    path('', include(router.urls)),
]