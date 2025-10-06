"""
Admin Control URL patterns
"""
from django.urls import path
from .views import (
    TradingSettingsView, ProfitLossScenarioListView, ProfitLossScenarioDetailView,
    ScenarioExecutionListView, execute_scenario, activate_scenario, deactivate_scenario,
    AdminDashboardView
)

app_name = 'admin_control'

urlpatterns = [
    # Trading settings
    path('settings/', TradingSettingsView.as_view(), name='trading_settings'),
    
    # Profit/Loss scenarios
    path('scenarios/', ProfitLossScenarioListView.as_view(), name='scenario_list'),
    path('scenarios/<int:pk>/', ProfitLossScenarioDetailView.as_view(), name='scenario_detail'),
    path('scenarios/<int:scenario_id>/execute/', execute_scenario, name='execute_scenario'),
    path('scenarios/<int:scenario_id>/activate/', activate_scenario, name='activate_scenario'),
    path('scenarios/<int:scenario_id>/deactivate/', deactivate_scenario, name='deactivate_scenario'),
    
    # Scenario executions
    path('executions/', ScenarioExecutionListView.as_view(), name='execution_list'),
    
    # Admin dashboard
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
]
