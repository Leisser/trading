from django.urls import path
from . import views

app_name = 'risk_management'

urlpatterns = [
    path('risk/', views.risk_list, name='risk_list'),
    path('risk/<int:pk>/', views.risk_detail, name='risk_detail'),
]
