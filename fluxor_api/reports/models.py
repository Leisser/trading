from django.db import models
from django.conf import settings
from decimal import Decimal
from django.utils import timezone

class Report(models.Model):
    """Model for generated reports"""
    
    REPORT_TYPES = [
        ('trading_summary', 'Trading Summary'),
        ('portfolio_performance', 'Portfolio Performance'),
        ('risk_analysis', 'Risk Analysis'),
        ('compliance_report', 'Compliance Report'),
        ('tax_report', 'Tax Report'),
        ('custom_report', 'Custom Report'),
    ]
    
    REPORT_FORMATS = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('json', 'JSON'),
        ('html', 'HTML'),
    ]
    
    REPORT_STATUS = [
        ('pending', 'Pending'),
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    ]
    
    # Report information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=25, choices=REPORT_TYPES)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Report parameters
    parameters = models.JSONField(default=dict, blank=True)  # Report-specific parameters
    date_range_start = models.DateTimeField(null=True, blank=True)
    date_range_end = models.DateTimeField(null=True, blank=True)
    
    # Report output
    format = models.CharField(max_length=10, choices=REPORT_FORMATS, default='pdf')
    file_path = models.CharField(max_length=500, null=True, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)  # bytes
    
    # Report status
    status = models.CharField(max_length=20, choices=REPORT_STATUS, default='pending')
    progress = models.IntegerField(default=0)  # 0-100
    error_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'report_type']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.report_type} ({self.status})"

class ReportTemplate(models.Model):
    """Model for report templates"""
    
    TEMPLATE_CATEGORIES = [
        ('trading', 'Trading Reports'),
        ('portfolio', 'Portfolio Reports'),
        ('risk', 'Risk Reports'),
        ('compliance', 'Compliance Reports'),
        ('custom', 'Custom Reports'),
    ]
    
    # Template information
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=TEMPLATE_CATEGORIES)
    description = models.TextField(blank=True)
    
    # Template configuration
    report_type = models.CharField(max_length=25, choices=Report.REPORT_TYPES)
    default_parameters = models.JSONField(default=dict, blank=True)
    template_config = models.JSONField(default=dict, blank=True)  # Template-specific configuration
    
    # Template settings
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    requires_subscription = models.BooleanField(default=False)
    
    # Usage tracking
    usage_count = models.IntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class ScheduledReport(models.Model):
    """Model for scheduled reports"""
    
    SCHEDULE_TYPES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ]
    
    # Schedule information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scheduled_reports')
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE, related_name='schedules')
    name = models.CharField(max_length=200)
    
    # Schedule configuration
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPES)
    schedule_config = models.JSONField(default=dict, blank=True)  # Cron-like configuration
    parameters = models.JSONField(default=dict, blank=True)
    
    # Output settings
    format = models.CharField(max_length=10, choices=Report.REPORT_FORMATS, default='pdf')
    email_recipients = models.JSONField(default=list, blank=True)
    auto_delete_after_days = models.IntegerField(null=True, blank=True)
    
    # Schedule status
    is_active = models.BooleanField(default=True)
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['next_run', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.schedule_type}"

class ReportAnalytics(models.Model):
    """Model for report analytics and metrics"""
    
    # Analytics data
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='report_analytics')
    report_type = models.CharField(max_length=25, choices=Report.REPORT_TYPES)
    
    # Usage metrics
    reports_generated = models.IntegerField(default=0)
    total_file_size = models.BigIntegerField(default=0)  # bytes
    average_generation_time = models.FloatField(null=True, blank=True)  # seconds
    
    # Performance metrics
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0'))  # percentage
    average_file_size = models.BigIntegerField(null=True, blank=True)
    
    # Time-based metrics
    last_generated = models.DateTimeField(null=True, blank=True)
    most_used_format = models.CharField(max_length=10, choices=Report.REPORT_FORMATS, null=True, blank=True)
    
    # Timestamps
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'report_type', 'period_start']
        ordering = ['-period_end']
    
    def __str__(self):
        return f"{self.user.email} - {self.report_type} ({self.period_start.date()})"

class ExportJob(models.Model):
    """Model for data export jobs"""
    
    EXPORT_TYPES = [
        ('trades', 'Trades Export'),
        ('orders', 'Orders Export'),
        ('positions', 'Positions Export'),
        ('portfolio', 'Portfolio Export'),
        ('transactions', 'Transactions Export'),
        ('custom', 'Custom Export'),
    ]
    
    EXPORT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # Export information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='export_jobs')
    export_type = models.CharField(max_length=20, choices=EXPORT_TYPES)
    name = models.CharField(max_length=200)
    
    # Export parameters
    parameters = models.JSONField(default=dict, blank=True)
    filters = models.JSONField(default=dict, blank=True)
    date_range_start = models.DateTimeField(null=True, blank=True)
    date_range_end = models.DateTimeField(null=True, blank=True)
    
    # Export output
    format = models.CharField(max_length=10, choices=Report.REPORT_FORMATS, default='csv')
    file_path = models.CharField(max_length=500, null=True, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    record_count = models.IntegerField(null=True, blank=True)
    
    # Export status
    status = models.CharField(max_length=20, choices=EXPORT_STATUS, default='pending')
    progress = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'export_type']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.export_type} ({self.status})"

class DashboardWidget(models.Model):
    """Model for dashboard widgets and charts"""
    
    WIDGET_TYPES = [
        ('chart', 'Chart'),
        ('metric', 'Metric'),
        ('table', 'Table'),
        ('gauge', 'Gauge'),
        ('progress', 'Progress Bar'),
        ('custom', 'Custom Widget'),
    ]
    
    CHART_TYPES = [
        ('line', 'Line Chart'),
        ('bar', 'Bar Chart'),
        ('pie', 'Pie Chart'),
        ('doughnut', 'Doughnut Chart'),
        ('area', 'Area Chart'),
        ('candlestick', 'Candlestick Chart'),
    ]
    
    # Widget information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dashboard_widgets')
    name = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    chart_type = models.CharField(max_length=20, choices=CHART_TYPES, null=True, blank=True)
    
    # Widget configuration
    data_source = models.CharField(max_length=100)  # e.g., 'trades', 'portfolio', 'custom'
    data_config = models.JSONField(default=dict, blank=True)
    display_config = models.JSONField(default=dict, blank=True)
    
    # Widget settings
    is_active = models.BooleanField(default=True)
    refresh_interval = models.IntegerField(null=True, blank=True)  # seconds
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    width = models.IntegerField(default=6)  # Bootstrap grid columns
    height = models.IntegerField(default=4)  # Bootstrap grid rows
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position_y', 'position_x']
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.widget_type}"

class ReportPermission(models.Model):
    """Model for report permissions and access control"""
    
    PERMISSION_TYPES = [
        ('view', 'View'),
        ('generate', 'Generate'),
        ('schedule', 'Schedule'),
        ('export', 'Export'),
        ('admin', 'Admin'),
    ]
    
    # Permission information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='report_permissions')
    report_type = models.CharField(max_length=25, choices=Report.REPORT_TYPES)
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPES)
    
    # Permission settings
    is_granted = models.BooleanField(default=True)
    granted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='granted_permissions')
    granted_at = models.DateTimeField(auto_now_add=True)
    
    # Permission constraints
    max_reports_per_day = models.IntegerField(null=True, blank=True)
    max_file_size = models.BigIntegerField(null=True, blank=True)  # bytes
    allowed_formats = models.JSONField(default=list, blank=True)
    
    # Timestamps
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'report_type', 'permission_type']
        ordering = ['user', 'report_type']
    
    def __str__(self):
        return f"{self.user.email} - {self.report_type} ({self.permission_type})"
