from django.urls import path
from .views import (
    TradeListCreateView, TradeDetailView, TradeStatsView, 
    CancelTradeView, TradeHistoryView
)
from . import crypto_views
from . import investment_views
from . import admin_views

app_name = 'trades'

urlpatterns = [
    # Basic trade operations
    path('trades/', TradeListCreateView.as_view(), name='trade_list_create'),
    path('trades/<int:pk>/', TradeDetailView.as_view(), name='trade_detail'),
    path('trades/<int:trade_id>/cancel/', CancelTradeView.as_view(), name='cancel_trade'),
    
    # Trade analytics and history
    path('trades/stats/', TradeStatsView.as_view(), name='trade_stats'),
    path('trades/history/', TradeHistoryView.as_view(), name='trade_history'),
    
    # Enhanced crypto endpoints from fluxor_backend
    path('cryptocurrencies/', crypto_views.CryptocurrencyListView.as_view(), name='cryptocurrency-list'),
    path('cryptocurrencies/<int:pk>/', crypto_views.CryptocurrencyDetailView.as_view(), name='cryptocurrency-detail'),
    path('wallet/', crypto_views.WalletView.as_view(), name='wallet'),
    path('execute-trade/', crypto_views.ExecuteTradeView.as_view(), name='execute-trade'),
    path('price-feed/', crypto_views.PriceFeedView.as_view(), name='price-feed'),
    path('trading-signals/', crypto_views.TradingSignalView.as_view(), name='trading-signals'),
    path('deposits/', crypto_views.DepositListView.as_view(), name='deposit-list'),
    path('withdrawals/', crypto_views.WithdrawalListView.as_view(), name='withdrawal-list'),
    path('notifications/', crypto_views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', crypto_views.NotificationDetailView.as_view(), name='notification-detail'),
    path('check-deposits/', crypto_views.check_deposits, name='check-deposits'),
    path('request-withdrawal/', crypto_views.request_withdrawal, name='request-withdrawal'),
    path('trading-stats/', crypto_views.get_trading_stats, name='trading-stats'),
    
    # New Crypto Wallet endpoints
    path('crypto-wallets/', crypto_views.CryptoWalletListView.as_view(), name='crypto-wallet-list'),
    path('crypto-wallets/<int:pk>/', crypto_views.CryptoWalletDetailView.as_view(), name='crypto-wallet-detail'),
    path('wallet-balances/', crypto_views.WalletBalanceView.as_view(), name='wallet-balances'),
    
    # New Crypto Swap endpoints
    path('crypto-swaps/', crypto_views.CryptoSwapListView.as_view(), name='crypto-swap-list'),
    path('crypto-swaps/<int:pk>/', crypto_views.CryptoSwapDetailView.as_view(), name='crypto-swap-detail'),
    path('swap-quote/', crypto_views.SwapQuoteView.as_view(), name='swap-quote'),
    path('execute-swap/', crypto_views.ExecuteSwapView.as_view(), name='execute-swap'),
    path('supported-tokens/', crypto_views.get_supported_tokens, name='supported-tokens'),
    path('swap-pairs/', crypto_views.get_swap_pairs, name='swap-pairs'),
    
    # New Crypto Payment endpoints
    path('crypto-payments/', crypto_views.CryptoPaymentListView.as_view(), name='crypto-payment-list'),
    path('crypto-payments/<int:pk>/', crypto_views.CryptoPaymentDetailView.as_view(), name='crypto-payment-detail'),
    path('create-payment/', crypto_views.CreatePaymentView.as_view(), name='create-payment'),
    path('verify-payment/', crypto_views.verify_payment, name='verify-payment'),
    
    # Crypto Investment endpoints
    path('crypto-indices/', investment_views.CryptoIndexListView.as_view(), name='crypto-index-list'),
    path('crypto-indices/<int:pk>/', investment_views.CryptoIndexDetailView.as_view(), name='crypto-index-detail'),
    path('crypto-indices/<int:index_id>/price-history/', investment_views.index_price_history, name='index-price-history'),
    
    # Investment management
    path('investments/', investment_views.CryptoInvestmentListView.as_view(), name='investment-list'),
    path('investments/<int:pk>/', investment_views.CryptoInvestmentDetailView.as_view(), name='investment-detail'),
    path('investments/<int:investment_id>/add-funds/', investment_views.add_investment_funds, name='add-investment-funds'),
    path('investments/<int:investment_id>/withdraw/', investment_views.withdraw_investment_funds, name='withdraw-investment-funds'),
    path('investments/<int:investment_id>/performance/', investment_views.investment_performance, name='investment-performance'),
    path('investments/<int:investment_id>/history/', investment_views.investment_history, name='investment-history'),
    
    # Portfolio analytics
    path('portfolio/allocation/', investment_views.portfolio_allocation, name='portfolio-allocation'),
]

# Admin URLs
admin_urlpatterns = [
    # Trading Settings
    path('admin/settings/', admin_views.AdminTradingSettingsView.as_view(), name='admin-trading-settings'),
    
    # Dashboard and Statistics
    path('admin/dashboard-stats/', admin_views.admin_dashboard_stats, name='admin-dashboard-stats'),
    path('admin/system-health/', admin_views.system_health_check, name='admin-system-health'),
    
    # Price Control
    path('admin/manual-price-control/', admin_views.manual_price_control, name='admin-manual-price-control'),
    
    # Scenarios
    path('admin/scenarios/', admin_views.ProfitLossScenarioListView.as_view(), name='admin-scenarios'),
    path('admin/scenarios/<int:pk>/', admin_views.ProfitLossScenarioDetailView.as_view(), name='admin-scenario-detail'),
    path('admin/execute-scenario/<int:scenario_id>/', admin_views.execute_scenario, name='admin-execute-scenario'),
    
    # Deposit Management
    path('admin/deposit-wallets/', admin_views.DepositWalletListView.as_view(), name='admin-deposit-wallets'),
    path('admin/deposit-wallets/<int:pk>/', admin_views.DepositWalletDetailView.as_view(), name='admin-deposit-wallet-detail'),
    path('admin/pending-deposits/', admin_views.PendingDepositsView.as_view(), name='admin-pending-deposits'),
    path('admin/approve-deposit/<int:deposit_id>/', admin_views.approve_deposit, name='admin-approve-deposit'),
    path('admin/reject-deposit/<int:deposit_id>/', admin_views.reject_deposit, name='admin-reject-deposit'),
    
    # Price Movement Logs
    path('admin/price-movements/', admin_views.recent_price_movements, name='admin-price-movements'),
]

# Combine all URL patterns
urlpatterns += admin_urlpatterns
