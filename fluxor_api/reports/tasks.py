import logging
from decimal import Decimal
from celery import shared_task
from django.utils import timezone
from django.db import transaction

logger = logging.getLogger(__name__)

@shared_task
def generate_scheduled_reports():
    """Generate all scheduled reports"""
    try:
        from .models import ScheduledReport
        
        # Get due scheduled reports
        due_reports = ScheduledReport.objects.filter(
            is_active=True,
            next_run__lte=timezone.now()
        ).select_related('user', 'template')
        
        for scheduled_report in due_reports:
            try:
                # Generate the report
                generate_scheduled_report.delay(scheduled_report.id)
                
            except Exception as e:
                logger.error(f"Error generating scheduled report {scheduled_report.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in generate_scheduled_reports: {str(e)}")
        raise

@shared_task
def generate_scheduled_report(scheduled_report_id):
    """Generate a specific scheduled report"""
    try:
        from .models import ScheduledReport, Report
        
        scheduled_report = ScheduledReport.objects.get(id=scheduled_report_id)
        
        # Generate the report
        report = Report.objects.create(
            user=scheduled_report.user,
            template=scheduled_report.template,
            title=scheduled_report.template.title,
            report_type=scheduled_report.template.report_type,
            parameters=scheduled_report.parameters,
            generated_at=timezone.now(),
            status='generated',
        )
        
        # Generate report content
        generate_report_content.delay(report.id)
        
        # Update next run time
        update_scheduled_report_next_run.delay(scheduled_report.id)
        
        # Send notification
        send_report_notification.delay(report.id)
        
        logger.info(f"Generated scheduled report {scheduled_report_id}")
        return report.id
        
    except ScheduledReport.DoesNotExist:
        logger.error(f"Scheduled report {scheduled_report_id} not found")
        return None
    except Exception as e:
        logger.error(f"Error generating scheduled report {scheduled_report_id}: {str(e)}")
        raise

@shared_task
def generate_report_content(report_id):
    """Generate content for a specific report"""
    try:
        from .models import Report
        
        report = Report.objects.get(id=report_id)
        
        # Generate content based on report type
        if report.report_type == 'portfolio_summary':
            content = generate_portfolio_summary_content(report)
        elif report.report_type == 'trading_activity':
            content = generate_trading_activity_content(report)
        elif report.report_type == 'performance_analysis':
            content = generate_performance_analysis_content(report)
        elif report.report_type == 'risk_analysis':
            content = generate_risk_analysis_content(report)
        else:
            content = generate_generic_content(report)
        
        # Update report with content
        report.content = content
        report.save()
        
        logger.info(f"Generated content for report {report_id}")
        return True
        
    except Report.DoesNotExist:
        logger.error(f"Report {report_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error generating content for report {report_id}: {str(e)}")
        raise

@shared_task
def update_scheduled_report_next_run(scheduled_report_id):
    """Update next run time for a scheduled report"""
    try:
        from .models import ScheduledReport
        
        scheduled_report = ScheduledReport.objects.get(id=scheduled_report_id)
        
        # Calculate next run time based on frequency
        if scheduled_report.frequency == 'daily':
            next_run = timezone.now() + timezone.timedelta(days=1)
        elif scheduled_report.frequency == 'weekly':
            next_run = timezone.now() + timezone.timedelta(weeks=1)
        elif scheduled_report.frequency == 'monthly':
            next_run = timezone.now() + timezone.timedelta(days=30)
        else:
            next_run = timezone.now() + timezone.timedelta(days=1)
        
        scheduled_report.next_run = next_run
        scheduled_report.save()
        
        logger.info(f"Updated next run time for scheduled report {scheduled_report_id}")
        return True
        
    except ScheduledReport.DoesNotExist:
        logger.error(f"Scheduled report {scheduled_report_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error updating next run time for scheduled report {scheduled_report_id}: {str(e)}")
        raise

@shared_task
def send_report_notification(report_id):
    """Send notification when report is generated"""
    try:
        from .models import Report
        
        report = Report.objects.get(id=report_id)
        
        # Send email notification
        send_report_email.delay(report.id)
        
        # Send in-app notification
        send_report_in_app_notification.delay(report.id)
        
        logger.info(f"Sent notification for report {report_id}")
        return True
        
    except Report.DoesNotExist:
        logger.error(f"Report {report_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending report notification: {str(e)}")
        raise

@shared_task
def send_report_email(report_id):
    """Send report via email"""
    try:
        from .models import Report
        from django.core.mail import send_mail
        from django.conf import settings
        
        report = Report.objects.get(id=report_id)
        
        subject = f"Report Generated: {report.title}"
        message = f"""
        Your report has been generated successfully.
        
        Report: {report.title}
        Type: {report.report_type}
        Generated: {report.generated_at}
        
        You can view the report in your dashboard.
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[report.user.email],
            fail_silently=False,
        )
        
        logger.info(f"Sent report email for report {report_id}")
        return True
        
    except Report.DoesNotExist:
        logger.error(f"Report {report_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending report email: {str(e)}")
        raise

@shared_task
def send_report_in_app_notification(report_id):
    """Send in-app notification for report"""
    try:
        from .models import Report
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        report = Report.objects.get(id=report_id)
        
        channel_layer = get_channel_layer()
        
        async_to_sync(channel_layer.group_send)(
            f"user_{report.user.id}",
            {
                "type": "report.notification",
                "report_id": report.id,
                "title": report.title,
                "message": f"Report '{report.title}' has been generated",
            }
        )
        
        logger.info(f"Sent in-app notification for report {report_id}")
        return True
        
    except Report.DoesNotExist:
        logger.error(f"Report {report_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending in-app notification: {str(e)}")
        raise

@shared_task
def export_report_data(report_id, export_format='csv'):
    """Export report data in specified format"""
    try:
        from .models import Report, ExportJob
        
        report = Report.objects.get(id=report_id)
        
        # Create export job
        export_job = ExportJob.objects.create(
            report=report,
            export_format=export_format,
            status='pending',
            created_at=timezone.now(),
        )
        
        # Process export
        process_export_job.delay(export_job.id)
        
        logger.info(f"Created export job for report {report_id}")
        return export_job.id
        
    except Report.DoesNotExist:
        logger.error(f"Report {report_id} not found")
        return None
    except Exception as e:
        logger.error(f"Error creating export job: {str(e)}")
        raise

@shared_task
def process_export_job(export_job_id):
    """Process an export job"""
    try:
        from .models import ExportJob
        
        export_job = ExportJob.objects.get(id=export_job_id)
        
        # Update status to processing
        export_job.status = 'processing'
        export_job.save()
        
        # Generate export file
        file_path = generate_export_file(export_job)
        
        # Update export job with file path
        export_job.file_path = file_path
        export_job.status = 'completed'
        export_job.completed_at = timezone.now()
        export_job.save()
        
        # Send notification
        send_export_notification.delay(export_job.id)
        
        logger.info(f"Processed export job {export_job_id}")
        return True
        
    except ExportJob.DoesNotExist:
        logger.error(f"Export job {export_job_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error processing export job {export_job_id}: {str(e)}")
        raise

@shared_task
def send_export_notification(export_job_id):
    """Send notification when export is completed"""
    try:
        from .models import ExportJob
        
        export_job = ExportJob.objects.get(id=export_job_id)
        
        # Send email notification
        send_export_email.delay(export_job.id)
        
        logger.info(f"Sent export notification for job {export_job_id}")
        return True
        
    except ExportJob.DoesNotExist:
        logger.error(f"Export job {export_job_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending export notification: {str(e)}")
        raise

@shared_task
def send_export_email(export_job_id):
    """Send export completion email"""
    try:
        from .models import ExportJob
        from django.core.mail import send_mail
        from django.conf import settings
        
        export_job = ExportJob.objects.get(id=export_job_id)
        
        subject = f"Export Completed: {export_job.report.title}"
        message = f"""
        Your report export has been completed.
        
        Report: {export_job.report.title}
        Format: {export_job.export_format}
        Completed: {export_job.completed_at}
        
        You can download the file from your dashboard.
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[export_job.report.user.email],
            fail_silently=False,
        )
        
        logger.info(f"Sent export email for job {export_job_id}")
        return True
        
    except ExportJob.DoesNotExist:
        logger.error(f"Export job {export_job_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending export email: {str(e)}")
        raise

@shared_task
def cleanup_old_reports():
    """Clean up old reports and exports"""
    try:
        from .models import Report, ExportJob
        
        # Keep reports for different periods
        cutoff_reports = timezone.now() - timezone.timedelta(days=90)
        cutoff_exports = timezone.now() - timezone.timedelta(days=30)
        
        # Delete old reports
        deleted_reports = Report.objects.filter(generated_at__lt=cutoff_reports).delete()
        
        # Delete old export jobs
        deleted_exports = ExportJob.objects.filter(created_at__lt=cutoff_exports).delete()
        
        logger.info(f"Cleaned up old reports: {deleted_reports[0]} reports, {deleted_exports[0]} exports")
        
        return True
        
    except Exception as e:
        logger.error(f"Error cleaning up old reports: {str(e)}")
        raise

def generate_portfolio_summary_content(report):
    """Generate portfolio summary report content"""
    return f"""
    Portfolio Summary Report
    
    Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
    User: {report.user.username}
    
    This report contains a summary of your portfolio performance,
    including total value, asset allocation, and recent activity.
    
    Report content would be generated based on actual portfolio data.
    """

def generate_trading_activity_content(report):
    """Generate trading activity report content"""
    return f"""
    Trading Activity Report
    
    Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
    User: {report.user.username}
    
    This report contains details of your recent trading activity,
    including orders, fills, and performance metrics.
    
    Report content would be generated based on actual trading data.
    """

def generate_performance_analysis_content(report):
    """Generate performance analysis report content"""
    return f"""
    Performance Analysis Report
    
    Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
    User: {report.user.username}
    
    This report contains detailed performance analysis,
    including returns, risk metrics, and benchmarking.
    
    Report content would be generated based on actual performance data.
    """

def generate_risk_analysis_content(report):
    """Generate risk analysis report content"""
    return f"""
    Risk Analysis Report
    
    Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
    User: {report.user.username}
    
    This report contains risk analysis and metrics,
    including VaR, drawdown, and risk factor analysis.
    
    Report content would be generated based on actual risk data.
    """

def generate_generic_content(report):
    """Generate generic report content"""
    return f"""
    {report.title}
    
    Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
    User: {report.user.username}
    Type: {report.report_type}
    
    This is a {report.report_type} report.
    
    Report content would be generated based on actual data.
    """

def generate_export_file(export_job):
    """Generate export file for a report"""
    # This would generate the actual export file
    # For now, return a placeholder path
    return f"/exports/report_{export_job.report.id}_{export_job.export_format}.{export_job.export_format}" 