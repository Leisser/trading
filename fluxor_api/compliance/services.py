from django.conf import settings
from decimal import Decimal
from datetime import datetime, timedelta

class ComplianceService:
    def __init__(self):
        self.config = getattr(settings, 'COMPLIANCE_CONFIG', {})

    def is_kyc_required(self, amount):
        threshold = Decimal(self.config.get('KYC_REQUIRED_AMOUNT', 1000))
        return amount >= threshold

    def is_suspicious(self, amount):
        suspicious = Decimal(self.config.get('SUSPICIOUS_AMOUNT', 10000))
        return amount >= suspicious

    def is_reporting_required(self, amount):
        reporting = Decimal(self.config.get('REPORTING_THRESHOLD', 5000))
        return amount >= reporting

    def aml_check(self, user, recent_transactions):
        # Example: flag if user has > threshold in last 24h
        threshold = Decimal(self.config.get('SUSPICIOUS_AMOUNT', 10000))
        now = datetime.now()
        total = sum([tx.amount for tx in recent_transactions if (now - tx.created_at).total_seconds() < 86400])
        return total >= threshold

    def generate_report(self, user, transactions):
        # Example: generate a compliance report
        report = {
            'user': user.email,
            'total_volume': sum([tx.amount for tx in transactions]),
            'suspicious': [tx.id for tx in transactions if self.is_suspicious(tx.amount)],
            'reporting_required': [tx.id for tx in transactions if self.is_reporting_required(tx.amount)],
        }
        return report 