from django.urls import path
from . import views

app_name = 'blockchain'

urlpatterns = [
    path('blockchain/', views.blockchain_list, name='blockchain_list'),
    path('blockchain/<int:pk>/', views.blockchain_detail, name='blockchain_detail'),
]
