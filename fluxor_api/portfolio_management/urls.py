"""
URL patterns for Portfolio Management API.
"""
from django.urls import path
from .views import (
    PortfolioListView, PortfolioDetailView, PortfolioSummaryView,
    PortfolioBalanceView, TransactionListView, PnLAnalyticsView,
    AssetAllocationView, RiskMetricsView, PerformanceComparisonView,
    rebalance_portfolio, portfolio_history
)

app_name = 'portfolio'

urlpatterns = [
    # Portfolio management
    path('portfolios/', PortfolioListView.as_view(), name='portfolio_list'),
    path('portfolios/<int:pk>/', PortfolioDetailView.as_view(), name='portfolio_detail'),
    path('summary/', PortfolioSummaryView.as_view(), name='portfolio_summary'),
    
    # Balances and transactions
    path('balances/', PortfolioBalanceView.as_view(), name='portfolio_balances'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    
    # Analytics and performance
    path('pnl/', PnLAnalyticsView.as_view(), name='pnl_analytics'),
    path('allocation/', AssetAllocationView.as_view(), name='asset_allocation'),
    path('risk/', RiskMetricsView.as_view(), name='risk_metrics'),
    path('performance/', PerformanceComparisonView.as_view(), name='performance_comparison'),
    
    # Portfolio operations
    path('rebalance/', rebalance_portfolio, name='rebalance_portfolio'),
    path('history/', portfolio_history, name='portfolio_history'),
]
