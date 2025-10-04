from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    ComplianceCheckSerializer, ComplianceCheckResponseSerializer,
    ComplianceReportSerializer, SuspiciousActivitySerializer,
    RegulatoryComplianceSerializer, ComplianceSettingsSerializer,
    ComplianceDocumentSerializer
)

# Create your views here.

class ComplianceCheckView(APIView):
    """
    Check compliance for a trade.
    
    This endpoint performs comprehensive compliance checks including
    AML, KYC, sanctions screening, and risk assessment.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=ComplianceCheckSerializer,
        responses={
            200: ComplianceCheckResponseSerializer,
            400: "Bad Request - Invalid trade parameters"
        },
        operation_description="Check compliance for a trade"
    )
    def post(self, request):
        serializer = ComplianceCheckSerializer(data=request.data)
        if serializer.is_valid():
            # Mock compliance check for demonstration
            trade_data = serializer.validated_data
            amount = float(trade_data['amount'])
            
            # Simple compliance logic
            aml_check = 'passed' if amount < 10000 else 'pending'
            kyc_status = 'verified' if request.user.kyc_verified else 'pending'
            sanctions_check = 'passed'  # Mock check
            risk_assessment = 'low' if amount < 5000 else 'medium'
            
            response = {
                'compliance_check_passed': aml_check == 'passed' and kyc_status == 'verified',
                'aml_check': aml_check,
                'kyc_status': kyc_status,
                'sanctions_check': sanctions_check,
                'risk_assessment': risk_assessment,
                'warnings': [],
                'required_documents': []
            }
            
            if amount > 10000 and not request.user.kyc_verified:
                response['warnings'].append('KYC verification required for large amounts')
                response['required_documents'].append('Proof of identity')
                response['required_documents'].append('Proof of address')
            
            response_serializer = ComplianceCheckResponseSerializer(response)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComplianceReportView(APIView):
    """
    Get compliance report.
    
    This endpoint provides comprehensive compliance reports including
    transaction summaries, AML metrics, KYC metrics, and regulatory updates.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'period',
                openapi.IN_QUERY,
                description="Report period (daily/weekly/monthly)",
                type=openapi.TYPE_STRING,
                default='monthly'
            )
        ],
        responses={
            200: ComplianceReportSerializer,
            401: "Authentication required"
        },
        operation_description="Get compliance report"
    )
    def get(self, request):
        period = request.GET.get('period', 'monthly')
        
        # Mock compliance report for demonstration
        report = {
            'report_id': 'CR123456789',
            'report_date': '2024-01-01',
            'period': period,
            'summary': {
                'total_transactions': 150,
                'total_volume': 75000.00,
                'suspicious_transactions': 2,
                'compliance_score': 98.5
            },
            'aml_metrics': {
                'checks_performed': 150,
                'suspicious_activity': 2,
                'false_positives': 1,
                'investigation_time': '2.5 hours'
            },
            'kyc_metrics': {
                'new_users': 25,
                'verifications_completed': 23,
                'pending_verifications': 2,
                'average_verification_time': '1.2 days'
            },
            'regulatory_updates': [
                {
                    'update_type': 'new_requirement',
                    'description': 'Enhanced due diligence for transactions over $10,000',
                    'effective_date': '2024-02-01'
                }
            ]
        }
        serializer = ComplianceReportSerializer(report)
        return Response(serializer.data)

class SuspiciousActivityView(APIView):
    """
    Get suspicious activity reports.
    
    This endpoint returns all suspicious activity reports including
    unusual volume, patterns, and other compliance alerts.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Suspicious activity reports retrieved successfully",
                examples={
                    "application/json": [
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
                    ]
                }
            )
        },
        operation_description="Get suspicious activity reports"
    )
    def get(self, request):
        # Mock suspicious activity for demonstration
        activities = [
            {
                'activity_id': 'SA123456789',
                'user_id': request.user.id,
                'activity_type': 'unusual_volume',
                'severity': 'medium',
                'description': 'Unusual trading volume detected',
                'details': {
                    'normal_volume': 1000.00,
                    'current_volume': 5000.00,
                    'increase_percent': 400
                },
                'risk_score': 0.75,
                'status': 'under_investigation',
                'reported_at': '2024-01-01T12:00:00Z',
                'investigation_notes': 'Pattern analysis in progress'
            }
        ]
        return Response(activities)

class RegulatoryComplianceView(APIView):
    """
    Get regulatory compliance status.
    
    This endpoint provides the overall regulatory compliance status
    including AML, KYC, and data protection compliance.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: RegulatoryComplianceSerializer,
            401: "Authentication required"
        },
        operation_description="Get regulatory compliance status"
    )
    def get(self, request):
        # Mock regulatory compliance for demonstration
        compliance = {
            'compliance_status': 'compliant',
            'last_assessment': '2024-01-01T12:00:00Z',
            'next_assessment': '2024-02-01T12:00:00Z',
            'regulations': {
                'aml': {
                    'status': 'compliant',
                    'last_check': '2024-01-01T12:00:00Z',
                    'requirements': ['Customer due diligence', 'Transaction monitoring'],
                    'compliance_score': 95.0
                },
                'kyc': {
                    'status': 'compliant',
                    'last_check': '2024-01-01T12:00:00Z',
                    'requirements': ['Identity verification', 'Document verification'],
                    'compliance_score': 98.0
                },
                'data_protection': {
                    'status': 'compliant',
                    'last_check': '2024-01-01T12:00:00Z',
                    'requirements': ['GDPR compliance', 'Data encryption'],
                    'compliance_score': 92.0
                }
            },
            'audit_trail': [
                {
                    'audit_id': 'A123456789',
                    'audit_type': 'compliance_review',
                    'auditor': 'Internal Compliance Team',
                    'date': '2024-01-01T12:00:00Z',
                    'result': 'passed'
                }
            ]
        }
        serializer = RegulatoryComplianceSerializer(compliance)
        return Response(serializer.data)

class ComplianceSettingsView(APIView):
    """
    Get and update compliance settings.
    
    This endpoint allows administrators to view and modify compliance
    settings including AML thresholds and screening requirements.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: ComplianceSettingsSerializer,
            401: "Authentication required"
        },
        operation_description="Get compliance settings"
    )
    def get(self, request):
        # Mock settings for demonstration
        settings = {
            'aml_threshold': 10000.00,
            'kyc_required': True,
            'enhanced_due_diligence': True,
            'transaction_monitoring': True,
            'sanctions_screening': True,
            'pep_screening': True,
            'data_retention_years': 7
        }
        serializer = ComplianceSettingsSerializer(settings)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=ComplianceSettingsSerializer,
        responses={
            200: openapi.Response(
                description="Compliance settings updated successfully",
                examples={
                    "application/json": {
                        "settings_updated": True,
                        "message": "Compliance settings updated successfully",
                        "new_settings": {
                            "aml_threshold": 10000.00,
                            "kyc_required": True,
                            "enhanced_due_diligence": True,
                            "transaction_monitoring": True,
                            "sanctions_screening": True,
                            "pep_screening": True,
                            "data_retention_years": 7
                        }
                    }
                }
            )
        },
        operation_description="Update compliance settings"
    )
    def put(self, request):
        serializer = ComplianceSettingsSerializer(data=request.data)
        if serializer.is_valid():
            # In a real implementation, save settings to database
            return Response({
                'settings_updated': True,
                'message': 'Compliance settings updated successfully',
                'new_settings': serializer.validated_data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComplianceDocumentUploadView(APIView):
    """
    Upload compliance documents.
    
    This endpoint allows users to upload KYC and compliance documents
    for verification. Supported file types: PDF, JPG, PNG.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=ComplianceDocumentSerializer,
        responses={
            200: openapi.Response(
                description="Compliance documents uploaded successfully",
                examples={
                    "application/json": {
                        "document_id": "DOC123456789",
                        "status": "uploaded",
                        "verification_status": "pending",
                        "uploaded_at": "2024-01-01T12:00:00Z",
                        "estimated_verification_time": "2-3 business days"
                    }
                }
            ),
            400: "Bad Request - Invalid files or validation errors"
        },
        operation_description="Upload compliance documents"
    )
    def post(self, request):
        serializer = ComplianceDocumentSerializer(data=request.data)
        if serializer.is_valid():
            # In a real implementation, save files and trigger verification process
            return Response({
                'document_id': 'DOC123456789',
                'status': 'uploaded',
                'verification_status': 'pending',
                'uploaded_at': '2024-01-01T12:00:00Z',
                'estimated_verification_time': '2-3 business days'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
