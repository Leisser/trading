from django.urls import path
from . import views

app_name = 'compliance'

urlpatterns = [
    path('compliance/', views.compliance_list, name='compliance_list'),
    path('compliance/<int:pk>/', views.compliance_detail, name='compliance_detail'),
]
