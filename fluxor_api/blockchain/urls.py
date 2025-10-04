from django.urls import path
from .views import (
    BlockchainHealthView, TransactionStatusView, NetworkStatsView,
    BlockInfoView, MempoolView, FeeEstimateView
)

app_name = 'blockchain'

urlpatterns = [
    # Blockchain health and monitoring
    path('blockchain/health/', BlockchainHealthView.as_view(), name='blockchain_health'),
    path('blockchain/stats/', NetworkStatsView.as_view(), name='network_stats'),
    path('blockchain/mempool/', MempoolView.as_view(), name='mempool'),
    path('blockchain/fees/', FeeEstimateView.as_view(), name='fee_estimates'),
    
    # Transaction and block information
    path('blockchain/transaction/', TransactionStatusView.as_view(), name='transaction_status'),
    path('blockchain/block/', BlockInfoView.as_view(), name='block_info'),
] 