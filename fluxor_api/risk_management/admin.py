from django.contrib import admin
from .models import RiskProfile

@admin.register(RiskProfile)
class RiskProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'risk_level', 'max_loss']
    list_filter = ['risk_level']
    search_fields = ['user__email']
