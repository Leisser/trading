from django.contrib import admin
from .models import KYCUpload


@admin.register(KYCUpload)
class KYCUploadAdmin(admin.ModelAdmin):
    """Admin configuration for KYC uploads"""
    
    list_display = [
        'user',
        'document_type',
        'original_filename',
        'file_size',
        'status',
        'uploaded_at',
        'verified_at',
    ]
    
    list_filter = [
        'document_type',
        'status',
        'uploaded_at',
        'verified_at',
    ]
    
    search_fields = [
        'user__email',
        'user__username',
        'original_filename',
        'verification_notes',
    ]
    
    readonly_fields = [
        'user',
        'document_type',
        'file',
        'original_filename',
        'file_size',
        'mime_type',
        'uploaded_at',
        'ip_address',
        'user_agent',
    ]
    
    fieldsets = (
        ('Upload Information', {
            'fields': (
                'user',
                'document_type',
                'file',
                'original_filename',
                'file_size',
                'mime_type',
                'uploaded_at',
            )
        }),
        ('Verification', {
            'fields': (
                'status',
                'verified_at',
                'verified_by',
                'verification_notes',
            )
        }),
        ('Security Information', {
            'fields': (
                'ip_address',
                'user_agent',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset"""
        return super().get_queryset(request).select_related('user', 'verified_by')
    
    def has_add_permission(self, request):
        """Disable adding uploads from admin"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Allow changing verification status"""
        return True
    
    def has_delete_permission(self, request, obj=None):
        """Allow deleting uploads"""
        return True