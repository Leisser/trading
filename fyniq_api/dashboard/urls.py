from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('stats/', views.dashboard_stats, name='dashboard_stats'),
    path('user-stats/', views.user_stats, name='user_stats'),
    path('recent-trades/', views.recent_trades, name='recent_trades'),
]
