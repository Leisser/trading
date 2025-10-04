from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'symbol', 'alert_type', 'target_price', 'status']
    list_filter = ['alert_type', 'status']
    search_fields = ['user__email', 'symbol']
