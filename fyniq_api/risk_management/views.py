from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    RiskAssessmentSerializer, RiskCheckSerializer, RiskCheckResponseSerializer,
    PortfolioRiskSerializer, RiskAlertSerializer, RiskReportSerializer,
    RiskSettingsSerializer
)

# Create your views here.

class RiskAssessmentView(APIView):
    """
    Get current user's risk assessment.
    
    This endpoint provides a comprehensive risk assessment including risk score,
    position limits, and loss limits based on user's trading history and profile.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: RiskAssessmentSerializer,
            401: "Authentication required"
        },
        operation_description="Get current user's risk assessment"
    )
    def get(self, request):
        # Mock data for demonstration
        assessment = {
            'user_id': request.user.id,
            'risk_score': 0.65,
            'risk_level': 'moderate',
            'max_position_size': 5000.00,
            'max_leverage': 3.0,
            'daily_loss_limit': 500.00,
            'weekly_loss_limit': 2000.00,
            'monthly_loss_limit': 5000.00,
            'assessment_date': '2024-01-01T12:00:00Z'
        }
        serializer = RiskAssessmentSerializer(assessment)
        return Response(serializer.data)

class RiskCheckView(APIView):
    """
    Check risk for a potential trade.
    
    This endpoint analyzes the risk of a potential trade and provides
    recommendations and warnings based on current risk parameters.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=RiskCheckSerializer,
        responses={
            200: RiskCheckResponseSerializer,
            400: "Bad Request - Invalid trade parameters"
        },
        operation_description="Check risk for a potential trade"
    )
    def post(self, request):
        serializer = RiskCheckSerializer(data=request.data)
        if serializer.is_valid():
            # Mock risk check for demonstration
            trade_data = serializer.validated_data
            amount = float(trade_data['amount'])
            leverage = float(trade_data['leverage'])
            
            # Simple risk calculation
            position_size = amount * leverage
            risk_score = min(0.9, (position_size / 10000) * leverage)
            
            response = {
                'risk_check_passed': risk_score < 0.8,
                'risk_score': round(risk_score, 2),
                'position_size': position_size,
                'margin_required': amount,
                'max_loss': amount * 0.5,  # Simplified calculation
                'warnings': [],
                'recommendations': []
            }
            
            if leverage > 5:
                response['warnings'].append('High leverage detected')
                response['recommendations'].append('Consider reducing leverage for lower risk')
            
            if position_size > 5000:
                response['warnings'].append('Large position size')
                response['recommendations'].append('Consider reducing position size')
            
            response_serializer = RiskCheckResponseSerializer(response)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PortfolioRiskView(APIView):
    """
    Get portfolio risk analysis.
    
    This endpoint provides comprehensive portfolio risk metrics including
    VaR, Sharpe ratio, maximum drawdown, and other risk indicators.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: PortfolioRiskSerializer,
            401: "Authentication required"
        },
        operation_description="Get portfolio risk analysis"
    )
    def get(self, request):
        # Mock portfolio risk data for demonstration
        portfolio_risk = {
            'total_value': 15000.00,
            'total_pnl': 1250.00,
            'total_pnl_percent': 9.09,
            'var_95': 750.00,
            'var_99': 1200.00,
            'max_drawdown': -8.5,
            'sharpe_ratio': 1.25,
            'beta': 0.85,
            'correlation': 0.72,
            'volatility': 0.15,
            'risk_metrics': {
                'current_risk': 0.45,
                'target_risk': 0.35,
                'risk_budget': 0.80
            }
        }
        serializer = PortfolioRiskSerializer(portfolio_risk)
        return Response(serializer.data)

class RiskAlertsView(APIView):
    """
    Get active risk alerts.
    
    This endpoint returns all active risk alerts for the current user,
    including position limits, loss limits, and other risk warnings.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Risk alerts retrieved successfully",
                examples={
                    "application/json": [
                        {
                            "alert_id": "RA123456789",
                            "alert_type": "position_limit",
                            "severity": "high",
                            "message": "Position size exceeds risk limits",
                            "details": {
                                "current_position": 5000.00,
                                "max_allowed": 3000.00,
                                "excess": 2000.00
                            },
                            "timestamp": "2024-01-01T12:00:00Z",
                            "status": "active"
                        }
                    ]
                }
            )
        },
        operation_description="Get active risk alerts for current user"
    )
    def get(self, request):
        # Mock risk alerts for demonstration
        alerts = [
            {
                'alert_id': 'RA123456789',
                'alert_type': 'position_limit',
                'severity': 'high',
                'message': 'Position size exceeds risk limits',
                'details': {
                    'current_position': 5000.00,
                    'max_allowed': 3000.00,
                    'excess': 2000.00
                },
                'timestamp': '2024-01-01T12:00:00Z',
                'status': 'active'
            }
        ]
        return Response(alerts)

class RiskSettingsView(APIView):
    """
    Get and update user risk settings.
    
    This endpoint allows users to view and modify their risk management
    settings including position limits, loss limits, and risk tolerance.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: RiskSettingsSerializer,
            401: "Authentication required"
        },
        operation_description="Get current user's risk settings"
    )
    def get(self, request):
        # Mock settings for demonstration
        settings = {
            'max_position_size': 5000.00,
            'max_leverage': 3.0,
            'daily_loss_limit': 500.00,
            'weekly_loss_limit': 2000.00,
            'monthly_loss_limit': 5000.00,
            'enable_stop_loss': True,
            'enable_take_profit': True,
            'risk_tolerance': 'moderate'
        }
        serializer = RiskSettingsSerializer(settings)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=RiskSettingsSerializer,
        responses={
            200: openapi.Response(
                description="Risk settings updated successfully",
                examples={
                    "application/json": {
                        "settings_updated": True,
                        "message": "Risk settings updated successfully",
                        "new_settings": {
                            "max_position_size": 5000.00,
                            "max_leverage": 3.0,
                            "daily_loss_limit": 500.00,
                            "weekly_loss_limit": 2000.00,
                            "monthly_loss_limit": 5000.00,
                            "enable_stop_loss": True,
                            "enable_take_profit": True,
                            "risk_tolerance": "moderate"
                        }
                    }
                }
            )
        },
        operation_description="Update current user's risk settings"
    )
    def put(self, request):
        serializer = RiskSettingsSerializer(data=request.data)
        if serializer.is_valid():
            # In a real implementation, save settings to database
            return Response({
                'settings_updated': True,
                'message': 'Risk settings updated successfully',
                'new_settings': serializer.validated_data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
