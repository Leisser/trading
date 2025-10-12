from django.urls import path
from . import views

app_name = 'wallets'

urlpatterns = [
    # User wallet endpoints
    path('wallet/', views.UserWalletView.as_view(), name='user_wallet'),
    path('balance/', views.wallet_balance, name='wallet_balance'),

    # Multi-currency wallet endpoints
    path('multi-currency/', views.MultiCurrencyWalletView.as_view(), name='multi_currency_wallet'),
    path('crypto-balances/', views.CryptoBalanceListView.as_view(), name='crypto_balances'),
    path('crypto-balances/add/', views.AddCryptoBalanceView.as_view(), name='add_crypto_balance'),

    # Deposit endpoints
    path('deposit/request/', views.DepositRequestView.as_view(), name='deposit_request'),
    path('deposit/wallets/', views.DepositWalletsView.as_view(), name='deposit_wallets'),

    # Withdrawal endpoints
    path('withdrawal/request/', views.WithdrawalRequestView.as_view(), name='withdrawal_request'),
]
