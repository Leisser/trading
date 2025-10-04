from rest_framework import serializers
from decimal import Decimal

class RiskAssessmentSerializer(serializers.Serializer):
    """
    Serializer for risk assessment data.
    
    Example Response:
    {
        "user_id": 1,
        "risk_score": 0.65,
        "risk_level": "moderate",
        "max_position_size": 5000.00,
        "max_leverage": 3.0,
        "daily_loss_limit": 500.00,
        "weekly_loss_limit": 2000.00,
        "monthly_loss_limit": 5000.00,
        "assessment_date": "2024-01-01T12:00:00Z"
    }
    """
    user_id = serializers.IntegerField(help_text="User ID")
    risk_score = serializers.DecimalField(
        max_digits=3, 
        decimal_places=2,
        min_value=0.0,
        max_value=1.0,
        help_text="Risk score (0.0 to 1.0)"
    )
    risk_level = serializers.ChoiceField(
        choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')],
        help_text="Risk level category"
    )
    max_position_size = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Maximum allowed position size in USD"
    )
    max_leverage = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Maximum allowed leverage"
    )
    daily_loss_limit = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Daily loss limit in USD"
    )
    weekly_loss_limit = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Weekly loss limit in USD"
    )
    monthly_loss_limit = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Monthly loss limit in USD"
    )
    assessment_date = serializers.DateTimeField(help_text="Assessment timestamp")

class RiskCheckSerializer(serializers.Serializer):
    """
    Serializer for risk check requests.
    
    Example Request:
    {
        "trade_type": "buy",
        "amount": 1000.00,
        "leverage": 2.0,
        "current_price": 45000.00
    }
    
    Example Response:
    {
        "risk_check_passed": true,
        "risk_score": 0.45,
        "position_size": 2000.00,
        "margin_required": 1000.00,
        "max_loss": 500.00,
        "warnings": [],
        "recommendations": ["Consider reducing leverage for lower risk"]
    }
    """
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
    leverage = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        min_value=1.0,
        max_value=10.0,
        help_text="Leverage multiplier"
    )
    current_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Current asset price"
    )

class RiskCheckResponseSerializer(serializers.Serializer):
    """
    Serializer for risk check responses.
    """
    risk_check_passed = serializers.BooleanField(help_text="Whether risk check passed")
    risk_score = serializers.DecimalField(max_digits=3, decimal_places=2, help_text="Calculated risk score")
    position_size = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Total position size")
    margin_required = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Required margin")
    max_loss = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Maximum potential loss")
    warnings = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of risk warnings"
    )
    recommendations = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of risk management recommendations"
    )

class PortfolioRiskSerializer(serializers.Serializer):
    """
    Serializer for portfolio risk analysis.
    
    Example Response:
    {
        "total_value": 15000.00,
        "total_pnl": 1250.00,
        "total_pnl_percent": 9.09,
        "var_95": 750.00,
        "var_99": 1200.00,
        "max_drawdown": -8.5,
        "sharpe_ratio": 1.25,
        "beta": 0.85,
        "correlation": 0.72,
        "volatility": 0.15,
        "risk_metrics": {
            "current_risk": 0.45,
            "target_risk": 0.35,
            "risk_budget": 0.80
        }
    }
    """
    total_value = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Total portfolio value")
    total_pnl = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Total profit/loss")
    total_pnl_percent = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Total P&L percentage")
    var_95 = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Value at Risk (95%)")
    var_99 = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Value at Risk (99%)")
    max_drawdown = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Maximum drawdown percentage")
    sharpe_ratio = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Sharpe ratio")
    beta = serializers.DecimalField(max_digits=5, decimal_places=2, help_text="Portfolio beta")
    correlation = serializers.DecimalField(max_digits=3, decimal_places=2, help_text="Correlation with market")
    volatility = serializers.DecimalField(max_digits=3, decimal_places=2, help_text="Portfolio volatility")
    risk_metrics = serializers.DictField(help_text="Additional risk metrics")

class RiskAlertSerializer(serializers.Serializer):
    """
    Serializer for risk alerts.
    
    Example Response:
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
    """
    alert_id = serializers.CharField(help_text="Unique alert identifier")
    alert_type = serializers.ChoiceField(
        choices=[
            ('position_limit', 'Position Limit'),
            ('loss_limit', 'Loss Limit'),
            ('leverage_limit', 'Leverage Limit'),
            ('volatility_alert', 'Volatility Alert'),
            ('correlation_alert', 'Correlation Alert')
        ],
        help_text="Type of risk alert"
    )
    severity = serializers.ChoiceField(
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')],
        help_text="Alert severity level"
    )
    message = serializers.CharField(help_text="Alert message")
    details = serializers.DictField(help_text="Alert details")
    timestamp = serializers.DateTimeField(help_text="Alert timestamp")
    status = serializers.ChoiceField(
        choices=[('active', 'Active'), ('acknowledged', 'Acknowledged'), ('resolved', 'Resolved')],
        help_text="Alert status"
    )

class RiskReportSerializer(serializers.Serializer):
    """
    Serializer for comprehensive risk reports.
    
    Example Response:
    {
        "report_id": "RR123456789",
        "report_date": "2024-01-01",
        "period": "daily",
        "summary": {
            "total_trades": 25,
            "winning_trades": 15,
            "losing_trades": 10,
            "win_rate": 60.0,
            "total_pnl": 1250.00
        },
        "risk_metrics": {
            "var_95": 750.00,
            "max_drawdown": -8.5,
            "sharpe_ratio": 1.25
        },
        "alerts": [
            {
                "alert_type": "position_limit",
                "severity": "medium",
                "message": "Position approaching limit"
            }
        ],
        "recommendations": [
            "Consider reducing position sizes",
            "Implement tighter stop losses"
        ]
    }
    """
    report_id = serializers.CharField(help_text="Unique report identifier")
    report_date = serializers.DateField(help_text="Report date")
    period = serializers.ChoiceField(
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        help_text="Report period"
    )
    summary = serializers.DictField(help_text="Trading summary")
    risk_metrics = serializers.DictField(help_text="Risk metrics")
    alerts = serializers.ListField(
        child=serializers.DictField(),
        help_text="Active risk alerts"
    )
    recommendations = serializers.ListField(
        child=serializers.CharField(),
        help_text="Risk management recommendations"
    )

class RiskSettingsSerializer(serializers.Serializer):
    """
    Serializer for user risk settings.
    
    Example Request:
    {
        "max_position_size": 5000.00,
        "max_leverage": 3.0,
        "daily_loss_limit": 500.00,
        "weekly_loss_limit": 2000.00,
        "monthly_loss_limit": 5000.00,
        "enable_stop_loss": true,
        "enable_take_profit": true,
        "risk_tolerance": "moderate"
    }
    
    Example Response:
    {
        "settings_updated": true,
        "message": "Risk settings updated successfully",
        "new_settings": {
            "max_position_size": 5000.00,
            "max_leverage": 3.0,
            "daily_loss_limit": 500.00,
            "weekly_loss_limit": 2000.00,
            "monthly_loss_limit": 5000.00,
            "enable_stop_loss": true,
            "enable_take_profit": true,
            "risk_tolerance": "moderate"
        }
    }
    """
    max_position_size = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=100.0,
        max_value=100000.0,
        help_text="Maximum position size in USD"
    )
    max_leverage = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        min_value=1.0,
        max_value=10.0,
        help_text="Maximum leverage allowed"
    )
    daily_loss_limit = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=10.0,
        help_text="Daily loss limit in USD"
    )
    weekly_loss_limit = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=50.0,
        help_text="Weekly loss limit in USD"
    )
    monthly_loss_limit = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=100.0,
        help_text="Monthly loss limit in USD"
    )
    enable_stop_loss = serializers.BooleanField(help_text="Enable automatic stop loss")
    enable_take_profit = serializers.BooleanField(help_text="Enable automatic take profit")
    risk_tolerance = serializers.ChoiceField(
        choices=[('conservative', 'Conservative'), ('moderate', 'Moderate'), ('aggressive', 'Aggressive')],
        help_text="User's risk tolerance level"
    ) 