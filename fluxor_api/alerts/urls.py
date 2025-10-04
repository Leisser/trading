from django.urls import path
from . import views

app_name = 'alerts'

urlpatterns = [
    path('alerts/', views.alert_list, name='alert_list'),
    path('alerts/<int:pk>/', views.alert_detail, name='alert_detail'),
]
