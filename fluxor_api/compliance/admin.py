from django.contrib import admin
from .models import ComplianceCheck

@admin.register(ComplianceCheck)
class ComplianceCheckAdmin(admin.ModelAdmin):
    list_display = ['user', 'check_type', 'status']
    list_filter = ['check_type', 'status']
    search_fields = ['user__email']
