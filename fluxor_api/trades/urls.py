from django.urls import path
from . import crypto_views

app_name = 'trades'

urlpatterns = [
    # Trading endpoints
    path('trades/', crypto_views.TradeListView.as_view(), name='trade_list'),
    path('trades/<int:pk>/', crypto_views.TradeDetailView.as_view(), name='trade_detail'),
    path('trades/create/', crypto_views.CreateTradeView.as_view(), name='create_trade'),
    path('trades/<int:pk>/update/', crypto_views.UpdateTradeView.as_view(), name='update_trade'),
    path('trades/<int:pk>/delete/', crypto_views.DeleteTradeView.as_view(), name='delete_trade'),
]
