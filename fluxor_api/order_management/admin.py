from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'symbol', 'order_type', 'amount', 'price', 'status']
    list_filter = ['order_type', 'status']
    search_fields = ['user__email', 'symbol']
