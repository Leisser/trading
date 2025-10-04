from django.urls import path
from . import views

app_name = 'trading_engine'

urlpatterns = [
    # Trading engine endpoints
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/create/', views.CreateOrderView.as_view(), name='create_order'),
    path('orders/<int:pk>/update/', views.UpdateOrderView.as_view(), name='update_order'),
    path('orders/<int:pk>/cancel/', views.CancelOrderView.as_view(), name='cancel_order'),
    path('positions/', views.PositionListView.as_view(), name='position_list'),
    path('positions/<int:pk>/', views.PositionDetailView.as_view(), name='position_detail'),
]
