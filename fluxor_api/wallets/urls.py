from django.urls import path
from . import views

app_name = 'wallets'

urlpatterns = [
    path('wallets/', views.wallet_list, name='wallet_list'),
    path('wallets/<int:pk>/', views.wallet_detail, name='wallet_detail'),
]
