from rest_framework import serializers
from decimal import Decimal

class ComplianceCheckSerializer(serializers.Serializer):
    """
    Serializer for compliance check requests.
    
    Example Request:
    {
        "user_id": 1,
        "trade_type": "buy",
        "amount": 1000.00,
        "source_of_funds": "salary",
        "purpose": "investment"
    }
    
    Example Response:
    {
        "compliance_check_passed": true,
        "aml_check": "passed",
        "kyc_status": "verified",
        "sanctions_check": "passed",
        "risk_assessment": "low",
        "warnings": [],
        "required_documents": []
    }
    """
    user_id = serializers.IntegerField(help_text="User ID")
    trade_type = serializers.ChoiceField(
        choices=[('buy', 'Buy'), ('sell', 'Sell')],
        help_text="Type of trade"
    )
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=10.0,
        help_text="Trade amount in USD"
    )
    source_of_funds = serializers.ChoiceField(
        choices=[
            ('salary', 'Salary'),
            ('investment', 'Investment Returns'),
            ('business', 'Business Income'),
            ('inheritance', 'Inheritance'),
            ('other', 'Other')
        ],
        help_text="Source of funds for the trade"
    )
    purpose = serializers.ChoiceField(
        choices=[
            ('investment', 'Investment'),
            ('trading', 'Trading'),
            ('savings', 'Savings'),
            ('other', 'Other')
        ],
        help_text="Purpose of the trade"
    )

class ComplianceCheckResponseSerializer(serializers.Serializer):
    """
    Serializer for compliance check responses.
    """
    compliance_check_passed = serializers.BooleanField(help_text="Whether compliance check passed")
    aml_check = serializers.ChoiceField(
        choices=[('passed', 'Passed'), ('failed', 'Failed'), ('pending', 'Pending')],
        help_text="Anti-Money Laundering check result"
    )
    kyc_status = serializers.ChoiceField(
        choices=[('verified', 'Verified'), ('pending', 'Pending'), ('rejected', 'Rejected')],
        help_text="Know Your Customer status"
    )
    sanctions_check = serializers.ChoiceField(
        choices=[('passed', 'Passed'), ('failed', 'Failed'), ('pending', 'Pending')],
        help_text="Sanctions check result"
    )
    risk_assessment = serializers.ChoiceField(
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        help_text="Risk assessment level"
    )
    warnings = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of compliance warnings"
    )
    required_documents = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of required documents"
    )

class ComplianceReportSerializer(serializers.Serializer):
    """
    Serializer for compliance reports.
    
    Example Response:
    {
        "report_id": "CR123456789",
        "report_date": "2024-01-01",
        "period": "monthly",
        "summary": {
            "total_transactions": 150,
            "total_volume": 75000.00,
            "suspicious_transactions": 2,
            "compliance_score": 98.5
        },
        "aml_metrics": {
            "checks_performed": 150,
            "suspicious_activity": 2,
            "false_positives": 1,
            "investigation_time": "2.5 hours"
        },
        "kyc_metrics": {
            "new_users": 25,
            "verifications_completed": 23,
            "pending_verifications": 2,
            "average_verification_time": "1.2 days"
        },
        "regulatory_updates": [
            {
                "update_type": "new_requirement",
                "description": "Enhanced due diligence for transactions over $10,000",
                "effective_date": "2024-02-01"
            }
        ]
    }
    """
    report_id = serializers.CharField(help_text="Unique report identifier")
    report_date = serializers.DateField(help_text="Report date")
    period = serializers.ChoiceField(
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        help_text="Report period"
    )
    summary = serializers.DictField(help_text="Compliance summary")
    aml_metrics = serializers.DictField(help_text="AML metrics")
    kyc_metrics = serializers.DictField(help_text="KYC metrics")
    regulatory_updates = serializers.ListField(
        child=serializers.DictField(),
        help_text="Recent regulatory updates"
    )

class SuspiciousActivitySerializer(serializers.Serializer):
    """
    Serializer for suspicious activity reports.
    
    Example Response:
    {
        "activity_id": "SA123456789",
        "user_id": 1,
        "activity_type": "unusual_volume",
        "severity": "medium",
        "description": "Unusual trading volume detected",
        "details": {
            "normal_volume": 1000.00,
            "current_volume": 5000.00,
            "increase_percent": 400
        },
        "risk_score": 0.75,
        "status": "under_investigation",
        "reported_at": "2024-01-01T12:00:00Z",
        "investigation_notes": "Pattern analysis in progress"
    }
    """
    activity_id = serializers.CharField(help_text="Unique activity identifier")
    user_id = serializers.IntegerField(help_text="User ID")
    activity_type = serializers.ChoiceField(
        choices=[
            ('unusual_volume', 'Unusual Volume'),
            ('unusual_pattern', 'Unusual Pattern'),
            ('high_risk_source', 'High Risk Source'),
            ('sanctions_match', 'Sanctions Match'),
            ('pep_match', 'PEP Match')
        ],
        help_text="Type of suspicious activity"
    )
    severity = serializers.ChoiceField(
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')],
        help_text="Activity severity level"
    )
    description = serializers.CharField(help_text="Activity description")
    details = serializers.DictField(help_text="Activity details")
    risk_score = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        min_value=0.0,
        max_value=1.0,
        help_text="Risk score (0.0 to 1.0)"
    )
    status = serializers.ChoiceField(
        choices=[
            ('detected', 'Detected'),
            ('under_investigation', 'Under Investigation'),
            ('resolved', 'Resolved'),
            ('false_positive', 'False Positive')
        ],
        help_text="Investigation status"
    )
    reported_at = serializers.DateTimeField(help_text="Detection timestamp")
    investigation_notes = serializers.CharField(help_text="Investigation notes")

class RegulatoryComplianceSerializer(serializers.Serializer):
    """
    Serializer for regulatory compliance status.
    
    Example Response:
    {
        "compliance_status": "compliant",
        "last_assessment": "2024-01-01T12:00:00Z",
        "next_assessment": "2024-02-01T12:00:00Z",
        "regulations": {
            "aml": {
                "status": "compliant",
                "last_check": "2024-01-01T12:00:00Z",
                "requirements": ["Customer due diligence", "Transaction monitoring"],
                "compliance_score": 95.0
            },
            "kyc": {
                "status": "compliant",
                "last_check": "2024-01-01T12:00:00Z",
                "requirements": ["Identity verification", "Document verification"],
                "compliance_score": 98.0
            },
            "data_protection": {
                "status": "compliant",
                "last_check": "2024-01-01T12:00:00Z",
                "requirements": ["GDPR compliance", "Data encryption"],
                "compliance_score": 92.0
            }
        },
        "audit_trail": [
            {
                "audit_id": "A123456789",
                "audit_type": "compliance_review",
                "auditor": "Internal Compliance Team",
                "date": "2024-01-01T12:00:00Z",
                "result": "passed"
            }
        ]
    }
    """
    compliance_status = serializers.ChoiceField(
        choices=[('compliant', 'Compliant'), ('non_compliant', 'Non-Compliant'), ('under_review', 'Under Review')],
        help_text="Overall compliance status"
    )
    last_assessment = serializers.DateTimeField(help_text="Last compliance assessment")
    next_assessment = serializers.DateTimeField(help_text="Next scheduled assessment")
    regulations = serializers.DictField(help_text="Regulatory compliance details")
    audit_trail = serializers.ListField(
        child=serializers.DictField(),
        help_text="Compliance audit trail"
    )

class ComplianceSettingsSerializer(serializers.Serializer):
    """
    Serializer for compliance settings.
    
    Example Request:
    {
        "aml_threshold": 10000.00,
        "kyc_required": true,
        "enhanced_due_diligence": true,
        "transaction_monitoring": true,
        "sanctions_screening": true,
        "pep_screening": true,
        "data_retention_years": 7
    }
    
    Example Response:
    {
        "settings_updated": true,
        "message": "Compliance settings updated successfully",
        "new_settings": {
            "aml_threshold": 10000.00,
            "kyc_required": true,
            "enhanced_due_diligence": true,
            "transaction_monitoring": true,
            "sanctions_screening": true,
            "pep_screening": true,
            "data_retention_years": 7
        }
    }
    """
    aml_threshold = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=1000.0,
        help_text="AML reporting threshold in USD"
    )
    kyc_required = serializers.BooleanField(help_text="KYC verification required")
    enhanced_due_diligence = serializers.BooleanField(help_text="Enhanced due diligence enabled")
    transaction_monitoring = serializers.BooleanField(help_text="Transaction monitoring enabled")
    sanctions_screening = serializers.BooleanField(help_text="Sanctions screening enabled")
    pep_screening = serializers.BooleanField(help_text="PEP screening enabled")
    data_retention_years = serializers.IntegerField(
        min_value=1,
        max_value=10,
        help_text="Data retention period in years"
    )

class ComplianceDocumentSerializer(serializers.Serializer):
    """
    Serializer for compliance document upload.
    
    Example Request:
    {
        "document_type": "proof_of_identity",
        "document": <file>,
        "description": "Passport for KYC verification"
    }
    
    Example Response:
    {
        "document_id": "DOC123456789",
        "status": "uploaded",
        "verification_status": "pending",
        "uploaded_at": "2024-01-01T12:00:00Z",
        "estimated_verification_time": "2-3 business days"
    }
    """
    document_type = serializers.ChoiceField(
        choices=[
            ('proof_of_identity', 'Proof of Identity'),
            ('proof_of_address', 'Proof of Address'),
            ('source_of_funds', 'Source of Funds'),
            ('bank_statement', 'Bank Statement'),
            ('tax_document', 'Tax Document'),
            ('other', 'Other')
        ],
        help_text="Type of compliance document"
    )
    document = serializers.FileField(help_text="Document file")
    description = serializers.CharField(help_text="Document description")
    
    def validate_document(self, value):
        """Validate document file."""
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size must be under 10MB")
        return value 