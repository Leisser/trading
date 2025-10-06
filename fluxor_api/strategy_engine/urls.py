"""
Strategy Engine URL patterns
"""
from django.urls import path
from .views import (
    TradingStrategyListView, TradingStrategyDetailView, StrategyExecutionListView,
    StrategyPerformanceListView, StrategyAlertListView, start_strategy, stop_strategy,
    execute_strategy, StrategyAnalyticsView, backtest_strategy
)

app_name = 'strategy_engine'

urlpatterns = [
    # Strategy management
    path('strategies/', TradingStrategyListView.as_view(), name='strategy_list'),
    path('strategies/<int:pk>/', TradingStrategyDetailView.as_view(), name='strategy_detail'),
    path('strategies/<int:strategy_id>/start/', start_strategy, name='start_strategy'),
    path('strategies/<int:strategy_id>/stop/', stop_strategy, name='stop_strategy'),
    path('strategies/<int:strategy_id>/execute/', execute_strategy, name='execute_strategy'),
    path('strategies/<int:strategy_id>/backtest/', backtest_strategy, name='backtest_strategy'),
    
    # Strategy data
    path('strategies/<int:strategy_id>/executions/', StrategyExecutionListView.as_view(), name='strategy_executions'),
    path('strategies/<int:strategy_id>/performance/', StrategyPerformanceListView.as_view(), name='strategy_performance'),
    path('strategies/<int:strategy_id>/alerts/', StrategyAlertListView.as_view(), name='strategy_alerts'),
    
    # Analytics
    path('analytics/', StrategyAnalyticsView.as_view(), name='strategy_analytics'),
]
