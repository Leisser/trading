"""
Investment Management URL patterns
"""
from django.urls import path
from .views import (
    InvestmentListView, InvestmentDetailView, InvestmentTransactionListView,
    CryptoIndexListView, CryptocurrencyListView, InvestmentPerformanceView,
    invest_in_index, invest_in_crypto, setup_dca, toggle_auto_compound
)

app_name = 'investments'

urlpatterns = [
    # Investment management
    path('investments/', InvestmentListView.as_view(), name='investment_list'),
    path('investments/<int:pk>/', InvestmentDetailView.as_view(), name='investment_detail'),
    path('investments/<int:investment_id>/transactions/', InvestmentTransactionListView.as_view(), name='investment_transactions'),
    
    # Available investment targets
    path('indices/', CryptoIndexListView.as_view(), name='crypto_index_list'),
    path('cryptocurrencies/', CryptocurrencyListView.as_view(), name='cryptocurrency_list'),
    
    # Investment operations
    path('indices/<int:index_id>/invest/', invest_in_index, name='invest_in_index'),
    path('cryptocurrencies/<int:crypto_id>/invest/', invest_in_crypto, name='invest_in_crypto'),
    path('investments/<int:investment_id>/setup-dca/', setup_dca, name='setup_dca'),
    path('investments/<int:investment_id>/toggle-compound/', toggle_auto_compound, name='toggle_auto_compound'),
    
    # Performance analytics
    path('performance/', InvestmentPerformanceView.as_view(), name='investment_performance'),
]
