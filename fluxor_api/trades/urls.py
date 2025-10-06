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
    
    # Include router URLs
    path('', include(router.urls)),
]