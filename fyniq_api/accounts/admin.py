from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, LoginHistory, AuditLog, Notification


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'full_name', 'is_verified', 'kyc_verified', 'role', 'is_active', 'is_banned', 'is_frozen', 'date_joined')
    list_filter = ('is_verified', 'kyc_verified', 'role', 'is_active', 'is_banned', 'is_frozen', 'date_joined')
    search_fields = ('email', 'full_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone_number', 'date_of_birth', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'is_verified', 'kyc_verified')}),
        ('Account Status', {'fields': ('is_banned', 'ban_reason', 'banned_at', 'banned_by', 'is_frozen', 'freeze_reason', 'frozen_at', 'frozen_by')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )
    
    actions = ['ban_users', 'unban_users', 'freeze_users', 'unfreeze_users']
    
    def ban_users(self, request, queryset):
        from .services import UserManagementService
        for user in queryset:
            UserManagementService.ban_user(user, request.user, 'Banned via admin action')
        self.message_user(request, f'{queryset.count()} users have been banned.')
    ban_users.short_description = "Ban selected users"
    
    def unban_users(self, request, queryset):
        from .services import UserManagementService
        for user in queryset:
            UserManagementService.unban_user(user, request.user, 'Unbanned via admin action')
        self.message_user(request, f'{queryset.count()} users have been unbanned.')
    unban_users.short_description = "Unban selected users"
    
    def freeze_users(self, request, queryset):
        from .services import UserManagementService
        for user in queryset:
            UserManagementService.freeze_user(user, request.user, 'Frozen via admin action')
        self.message_user(request, f'{queryset.count()} users have been frozen.')
    freeze_users.short_description = "Freeze selected users"
    
    def unfreeze_users(self, request, queryset):
        from .services import UserManagementService
        for user in queryset:
            UserManagementService.unfreeze_user(user, request.user, 'Unfrozen via admin action')
        self.message_user(request, f'{queryset.count()} users have been unfrozen.')
    unfreeze_users.short_description = "Unfreeze selected users"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_currency', 'notifications_enabled', 'two_factor_enabled', 'created_at')
    list_filter = ('default_currency', 'notifications_enabled', 'two_factor_enabled', 'created_at')
    search_fields = ('user__email', 'user__full_name')


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'login_time', 'success')
    list_filter = ('success', 'login_time')
    search_fields = ('user__email', 'ip_address')
    readonly_fields = ('user', 'ip_address', 'user_agent', 'login_time', 'success')
    ordering = ('-login_time',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'admin_user', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__email', 'admin_user__email', 'action')
    readonly_fields = ('user', 'admin_user', 'action', 'details', 'ip_address', 'user_agent', 'timestamp')
    ordering = ('-timestamp',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'priority', 'is_read', 'sent_at')
    list_filter = ('notification_type', 'priority', 'is_read', 'sent_at')
    search_fields = ('user__email', 'title', 'message')
    readonly_fields = ('sent_at', 'read_at')
    ordering = ('-sent_at',)


admin.site.register(User, UserAdmin) 