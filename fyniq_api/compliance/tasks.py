import logging
from decimal import Decimal
from celery import shared_task
from django.utils import timezone
from django.db import transaction

logger = logging.getLogger(__name__)

@shared_task
def run_compliance_checks():
    """Run all compliance checks"""
    try:
        # Run KYC checks
        run_kyc_checks.delay()
        
        # Run AML checks
        run_aml_checks.delay()
        
        # Run trading compliance checks
        run_trading_compliance_checks.delay()
        
        # Run regulatory reporting
        run_regulatory_reporting.delay()
        
        return True
        
    except Exception as e:
        logger.error(f"Error in run_compliance_checks: {str(e)}")
        raise

@shared_task
def run_kyc_checks():
    """Run KYC (Know Your Customer) checks"""
    try:
        from accounts.models import User
        from .models import KYCVerification
        
        # Get users pending KYC verification
        pending_kyc = KYCVerification.objects.filter(
            status='pending'
        ).select_related('user')
        
        for kyc in pending_kyc:
            try:
                # Process KYC verification
                process_kyc_verification.delay(kyc.id)
                
            except Exception as e:
                logger.error(f"Error processing KYC {kyc.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in run_kyc_checks: {str(e)}")
        raise

@shared_task
def process_kyc_verification(kyc_id):
    """Process a specific KYC verification"""
    try:
        from .models import KYCVerification
        
        kyc = KYCVerification.objects.get(id=kyc_id)
        
        # Simulate KYC verification process
        # In a real implementation, this would integrate with KYC service providers
        
        # For now, just mark as approved after a delay
        kyc.status = 'approved'
        kyc.verified_at = timezone.now()
        kyc.save()
        
        # Update user status
        user = kyc.user
        user.is_verified = True
        user.save()
        
        logger.info(f"KYC verification {kyc_id} approved for user {user.id}")
        return True
        
    except KYCVerification.DoesNotExist:
        logger.error(f"KYC verification {kyc_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error processing KYC verification {kyc_id}: {str(e)}")
        raise

@shared_task
def run_aml_checks():
    """Run AML (Anti-Money Laundering) checks"""
    try:
        from .models import AMLCheck, Transaction
        
        # Get recent transactions for AML screening
        recent_transactions = Transaction.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(hours=1)
        ).select_related('user')
        
        for transaction in recent_transactions:
            try:
                # Run AML check for this transaction
                run_transaction_aml_check.delay(transaction.id)
                
            except Exception as e:
                logger.error(f"Error running AML check for transaction {transaction.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in run_aml_checks: {str(e)}")
        raise

@shared_task
def run_transaction_aml_check(transaction_id):
    """Run AML check for a specific transaction"""
    try:
        from .models import Transaction, AMLCheck
        
        transaction = Transaction.objects.get(id=transaction_id)
        
        # Simulate AML screening
        # In a real implementation, this would integrate with AML screening services
        
        # Check for suspicious patterns
        is_suspicious = check_suspicious_patterns(transaction)
        
        # Create AML check record
        aml_check = AMLCheck.objects.create(
            transaction=transaction,
            check_type='transaction_screening',
            status='passed' if not is_suspicious else 'flagged',
            risk_score=Decimal('0.1') if not is_suspicious else Decimal('0.8'),
            details={'suspicious': is_suspicious},
            checked_at=timezone.now(),
        )
        
        if is_suspicious:
            # Create compliance alert
            create_compliance_alert.delay(
                alert_type='suspicious_transaction',
                transaction_id=transaction.id,
                severity='high',
                description=f"Suspicious transaction detected: {transaction.transaction_id}"
            )
        
        logger.info(f"AML check completed for transaction {transaction_id}: {'flagged' if is_suspicious else 'passed'}")
        return True
        
    except Transaction.DoesNotExist:
        logger.error(f"Transaction {transaction_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error running AML check for transaction {transaction_id}: {str(e)}")
        raise

@shared_task
def run_trading_compliance_checks():
    """Run trading compliance checks"""
    try:
        from order_management.models import Order
        from .models import TradingComplianceCheck
        
        # Get recent orders for compliance checking
        recent_orders = Order.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(hours=1)
        ).select_related('user')
        
        for order in recent_orders:
            try:
                # Run compliance check for this order
                run_order_compliance_check.delay(order.id)
                
            except Exception as e:
                logger.error(f"Error running compliance check for order {order.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in run_trading_compliance_checks: {str(e)}")
        raise

@shared_task
def run_order_compliance_check(order_id):
    """Run compliance check for a specific order"""
    try:
        from order_management.models import Order
        from .models import TradingComplianceCheck
        
        order = Order.objects.get(id=order_id)
        
        # Check for various compliance issues
        violations = []
        
        # Check for wash trading
        if check_wash_trading(order):
            violations.append('wash_trading')
        
        # Check for market manipulation
        if check_market_manipulation(order):
            violations.append('market_manipulation')
        
        # Check for insider trading
        if check_insider_trading(order):
            violations.append('insider_trading')
        
        # Create compliance check record
        compliance_check = TradingComplianceCheck.objects.create(
            order=order,
            check_type='order_screening',
            status='passed' if not violations else 'violation',
            violations=violations,
            checked_at=timezone.now(),
        )
        
        if violations:
            # Create compliance alert
            create_compliance_alert.delay(
                alert_type='trading_violation',
                order_id=order.id,
                severity='high',
                description=f"Trading compliance violation detected: {', '.join(violations)}"
            )
        
        logger.info(f"Compliance check completed for order {order_id}: {'violation' if violations else 'passed'}")
        return True
        
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error running compliance check for order {order_id}: {str(e)}")
        raise

@shared_task
def run_regulatory_reporting():
    """Run regulatory reporting tasks"""
    try:
        # Generate regulatory reports
        generate_regulatory_reports.delay()
        
        # Submit reports to regulators
        submit_regulatory_reports.delay()
        
        return True
        
    except Exception as e:
        logger.error(f"Error in run_regulatory_reporting: {str(e)}")
        raise

@shared_task
def generate_regulatory_reports():
    """Generate regulatory reports"""
    try:
        from .models import RegulatoryReport
        
        # Generate different types of reports
        report_types = ['daily', 'weekly', 'monthly']
        
        for report_type in report_types:
            try:
                generate_report.delay(report_type)
                
            except Exception as e:
                logger.error(f"Error generating {report_type} report: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in generate_regulatory_reports: {str(e)}")
        raise

@shared_task
def generate_report(report_type):
    """Generate a specific regulatory report"""
    try:
        from .models import RegulatoryReport
        
        # Generate report content
        report_content = generate_report_content(report_type)
        
        # Create report record
        report = RegulatoryReport.objects.create(
            report_type=report_type,
            title=f"{report_type.title()} Regulatory Report",
            content=report_content,
            generated_at=timezone.now(),
            status='generated',
        )
        
        logger.info(f"Generated {report_type} regulatory report")
        return report.id
        
    except Exception as e:
        logger.error(f"Error generating {report_type} report: {str(e)}")
        raise

@shared_task
def submit_regulatory_reports():
    """Submit regulatory reports to authorities"""
    try:
        from .models import RegulatoryReport
        
        # Get reports ready for submission
        pending_reports = RegulatoryReport.objects.filter(
            status='generated',
            generated_at__gte=timezone.now() - timezone.timedelta(hours=24)
        )
        
        for report in pending_reports:
            try:
                # Submit report
                submit_report.delay(report.id)
                
            except Exception as e:
                logger.error(f"Error submitting report {report.id}: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error in submit_regulatory_reports: {str(e)}")
        raise

@shared_task
def submit_report(report_id):
    """Submit a specific regulatory report"""
    try:
        from .models import RegulatoryReport
        
        report = RegulatoryReport.objects.get(id=report_id)
        
        # Simulate report submission
        # In a real implementation, this would submit to regulatory APIs
        
        report.status = 'submitted'
        report.submitted_at = timezone.now()
        report.save()
        
        logger.info(f"Submitted regulatory report {report_id}")
        return True
        
    except RegulatoryReport.DoesNotExist:
        logger.error(f"Regulatory report {report_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error submitting report {report_id}: {str(e)}")
        raise

@shared_task
def create_compliance_alert(alert_type, severity, description, **kwargs):
    """Create a compliance alert"""
    try:
        from .models import ComplianceAlert
        
        # Create compliance alert
        alert = ComplianceAlert.objects.create(
            alert_type=alert_type,
            severity=severity,
            description=description,
            details=kwargs,
            created_at=timezone.now(),
        )
        
        # Send notification to compliance team
        notify_compliance_team.delay(alert.id)
        
        logger.info(f"Created compliance alert: {alert_type} - {severity}")
        return alert.id
        
    except Exception as e:
        logger.error(f"Error creating compliance alert: {str(e)}")
        raise

@shared_task
def notify_compliance_team(alert_id):
    """Notify compliance team of an alert"""
    try:
        from .models import ComplianceAlert
        
        alert = ComplianceAlert.objects.get(id=alert_id)
        
        # Send email notification
        send_compliance_email.delay(alert.id)
        
        # Send Slack notification (if configured)
        send_compliance_slack.delay(alert.id)
        
        logger.info(f"Notified compliance team of alert {alert_id}")
        return True
        
    except ComplianceAlert.DoesNotExist:
        logger.error(f"Compliance alert {alert_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error notifying compliance team: {str(e)}")
        raise

@shared_task
def send_compliance_email(alert_id):
    """Send compliance alert email"""
    try:
        from .models import ComplianceAlert
        from django.core.mail import send_mail
        from django.conf import settings
        
        alert = ComplianceAlert.objects.get(id=alert_id)
        
        subject = f"Compliance Alert: {alert.alert_type}"
        message = f"""
        Compliance Alert
        
        Type: {alert.alert_type}
        Severity: {alert.severity}
        Description: {alert.description}
        Created: {alert.created_at}
        
        Please review and take appropriate action.
        """
        
        # Send to compliance team
        compliance_emails = getattr(settings, 'COMPLIANCE_EMAILS', ['compliance@example.com'])
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=compliance_emails,
            fail_silently=False,
        )
        
        logger.info(f"Sent compliance email for alert {alert_id}")
        return True
        
    except ComplianceAlert.DoesNotExist:
        logger.error(f"Compliance alert {alert_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending compliance email: {str(e)}")
        raise

@shared_task
def send_compliance_slack(alert_id):
    """Send compliance alert to Slack"""
    try:
        from .models import ComplianceAlert
        
        alert = ComplianceAlert.objects.get(id=alert_id)
        
        # This would integrate with Slack API
        # For now, just log the notification
        logger.info(f"Slack notification for compliance alert {alert_id}: {alert.alert_type}")
        return True
        
    except ComplianceAlert.DoesNotExist:
        logger.error(f"Compliance alert {alert_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending compliance Slack notification: {str(e)}")
        raise

def check_suspicious_patterns(transaction):
    """Check for suspicious transaction patterns"""
    # Simplified suspicious pattern detection
    # In a real implementation, this would use sophisticated algorithms
    
    # Check for large amounts
    if transaction.amount > Decimal('10000'):
        return True
    
    # Check for frequent small transactions
    recent_transactions = transaction.user.transactions.filter(
        created_at__gte=timezone.now() - timezone.timedelta(hours=1)
    ).count()
    
    if recent_transactions > 10:
        return True
    
    return False

def check_wash_trading(order):
    """Check for wash trading patterns"""
    # Simplified wash trading detection
    # In a real implementation, this would analyze trading patterns
    
    # Check for rapid buy/sell cycles
    recent_orders = order.user.orders.filter(
        trading_pair=order.trading_pair,
        created_at__gte=timezone.now() - timezone.timedelta(minutes=5)
    )
    
    if recent_orders.count() > 5:
        return True
    
    return False

def check_market_manipulation(order):
    """Check for market manipulation patterns"""
    # Simplified market manipulation detection
    # In a real implementation, this would analyze order patterns
    
    # Check for large orders that could move the market
    if order.quantity * (order.price or Decimal('50000')) > Decimal('100000'):
        return True
    
    return False

def check_insider_trading(order):
    """Check for insider trading patterns"""
    # Simplified insider trading detection
    # In a real implementation, this would analyze timing and patterns
    
    # Check for orders placed during unusual hours
    hour = order.created_at.hour
    if hour < 6 or hour > 22:  # Outside normal trading hours
        return True
    
    return False

def generate_report_content(report_type):
    """Generate regulatory report content"""
    return f"""
    Regulatory Report - {report_type.title()}
    
    Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    This is a {report_type} regulatory report containing:
    - Transaction summaries
    - User activity
    - Compliance metrics
    - Risk assessments
    
    Report content would be generated based on actual data.
    """ 