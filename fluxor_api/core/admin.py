from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from datetime import timedelta
from accounts.models import User, LoginHistory
from wallets.models import BTCWallet, Transaction, WithdrawalRequest

class RecentActivityFilter(SimpleListFilter):
    title = 'Recent Activity'
    parameter_name = 'recent_activity'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('week', 'This Week'),
            ('month', 'This Month'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(created_at__date=timezone.now().date())
        elif self.value() == 'week':
            return queryset.filter(created_at__gte=timezone.now() - timedelta(days=7))
        elif self.value() == 'month':
            return queryset.filter(created_at__gte=timezone.now() - timedelta(days=30))

# LoginHistory is already registered in accounts.admin
# @admin.register(LoginHistory)
# class LoginHistoryAdmin(admin.ModelAdmin):
#     list_display = ('user', 'ip_address', 'login_time', 'success')
#     list_filter = ('success', 'login_time', RecentActivityFilter)
#     search_fields = ('user__email', 'ip_address')
#     readonly_fields = ('user', 'ip_address', 'user_agent', 'login_time', 'success')
#     ordering = ('-login_time',) 