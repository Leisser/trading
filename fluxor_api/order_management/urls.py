from django.urls import path
from . import views

app_name = 'order_management'

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
]
