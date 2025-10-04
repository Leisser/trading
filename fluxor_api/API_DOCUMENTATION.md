# Fluxor Trading API Documentation

## Overview

The Fluxor Trading API is a comprehensive cryptocurrency trading platform that provides real-time market data, advanced trading algorithms, risk management, and compliance features. This API is built with Django REST Framework and includes WebSocket support for real-time updates.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

## API Endpoints

### 1. User Management

#### 1.1 Register User
**POST** `/accounts/register/`

Register a new user account.

**Request Body:**
```json
{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "phone_number": "+1234567890"
}
```

**Response (201):**
```json
{
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "message": "User registered successfully"
}
```

#### 1.2 Login User
**POST** `/accounts/login/`

Authenticate user and return access token.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Response (200):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "full_name": "John Doe"
    }
}
```

#### 1.3 Get User Profile
**GET** `/accounts/profile/`

Get current user's profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "date_of_birth": "1990-01-01",
    "country": "US",
    "is_verified": true,
    "kyc_verified": false,
    "role": "user",
    "date_joined": "2024-01-01T00:00:00Z"
}
```

#### 1.4 Update User Profile
**PUT** `/accounts/profile/`

Update current user's profile information.

**Request Body:**
```json
{
    "full_name": "John Doe Updated",
    "phone_number": "+1234567890",
    "date_of_birth": "1990-01-01",
    "country": "US"
}
```

#### 1.5 Change Password
**POST** `/accounts/password/change/`

Change current user's password.

**Request Body:**
```json
{
    "current_password": "oldpassword123",
    "new_password": "newpassword123"
}
```

#### 1.6 Get Login History
**GET** `/accounts/login-history/`

Get paginated login history for current user.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20)

**Response (200):**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/accounts/login-history/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0...",
            "timestamp": "2024-01-01T12:00:00Z",
            "success": true
        }
    ]
}
```

#### 1.7 Get User Settings
**GET** `/accounts/settings/`

Get current user's notification settings.

**Response (200):**
```json
{
    "email_notifications": true,
    "trade_alerts": true,
    "price_alerts": false
}
```

#### 1.8 Update User Settings
**PUT** `/accounts/settings/`

Update current user's notification settings.

**Request Body:**
```json
{
    "email_notifications": true,
    "trade_alerts": true,
    "price_alerts": false
}
```

#### 1.9 Upload KYC Documents
**POST** `/accounts/kyc/upload/`

Upload KYC verification documents.

**Request Body (multipart/form-data):**
```
id_document: <file>
address_document: <file>
selfie: <file>
```

**Response (200):**
```json
{
    "message": "KYC documents uploaded successfully",
    "verification_status": "pending",
    "estimated_verification_time": "2-3 business days"
}
```

#### 1.10 Logout
**POST** `/accounts/logout/`

Logout current user and invalidate session.

**Response (200):**
```json
{
    "message": "Logged out successfully"
}
```

### 2. Trading

#### 2.1 Create Trade
**POST** `/trades/`

Create a new trade.

**Request Body:**
```json
{
    "trade_type": "buy",
    "btc_amount": "0.001",
    "usd_price": "45000.00"
}
```

**Response (201):**
```json
{
    "id": 1,
    "user": 1,
    "user_email": "user@example.com",
    "trade_type": "buy",
    "btc_amount": "0.001",
    "usd_price": "45000.00",
    "status": "completed",
    "timestamp": "2024-01-01T12:00:00Z",
    "total_value": "45.00"
}
```

#### 2.2 Get Trade History
**GET** `/trades/`

Get paginated trade history.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20)
- `trade_type` (optional): Filter by trade type (buy/sell)
- `status` (optional): Filter by status (completed/pending/cancelled)

**Response (200):**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/trades/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "trade_type": "buy",
            "btc_amount": "0.001",
            "usd_price": "45000.00",
            "status": "completed",
            "timestamp": "2024-01-01T12:00:00Z",
            "pnl": 150.00,
            "roi": 3.33
        }
    ]
}
```

#### 2.3 Advanced Trade Execution
**POST** `/trading-engine/advanced-trade/`

Execute advanced trade with leverage and risk management.

**Request Body:**
```json
{
    "trade_type": "buy",
    "amount": 1000.00,
    "leverage": 2.0,
    "stop_loss": 44000.00,
    "take_profit": 46000.00
}
```

**Response (200):**
```json
{
    "status": "Trade executed (simulated)",
    "trade_id": "T123456789",
    "executed_price": 45000.00,
    "btc_amount": "0.04444444",
    "leverage_used": 2.0,
    "position_size": 2000.00,
    "risk_check": "passed",
    "compliance_check": "passed",
    "stop_loss": 44000.00,
    "take_profit": 46000.00,
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 3. Market Data

#### 3.1 Get Real-time Price
**GET** `/trading-engine/price-feed/`

Get real-time price data from multiple sources.

**Query Parameters:**
- `symbol` (optional): Trading pair (default: BTC/USDT)

**Response (200):**
```json
{
    "symbol": "BTC/USDT",
    "binance_price": 45000.00,
    "coingecko_price": 44985.50,
    "price_change_24h": 2.5,
    "volume_24h": 2500000000,
    "high_24h": 45500.00,
    "low_24h": 44000.00,
    "timestamp": "2024-01-01T12:00:00Z"
}
```

#### 3.2 Get Trading Signals
**GET** `/trading-engine/signals/`

Get trading signals from algorithms.

**Response (200):**
```json
{
    "signal": "buy",
    "confidence": 0.85,
    "indicators": {
        "rsi": 35.2,
        "sma": 44800.00,
        "ema": 44950.00,
        "macd": 150.00
    },
    "reasoning": "RSI indicates oversold conditions, MACD shows bullish momentum",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

#### 3.3 Get OHLCV Data
**GET** `/trading-engine/ohlcv/`

Get OHLCV (Open, High, Low, Close, Volume) data.

**Query Parameters:**
- `symbol` (optional): Trading pair (default: BTC/USDT)
- `timeframe` (optional): Timeframe (1m, 5m, 15m, 1h, 4h, 1d, default: 1h)
- `limit` (optional): Number of candles (default: 100)

**Response (200):**
```json
{
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "data": [
        {
            "timestamp": "2024-01-01T12:00:00Z",
            "open": 45000.00,
            "high": 45100.00,
            "low": 44900.00,
            "close": 45050.00,
            "volume": 1250.50
        }
    ]
}
```

#### 3.4 Get Technical Indicators
**GET** `/trading-engine/indicators/`

Get technical indicators data.

**Response (200):**
```json
{
    "symbol": "BTC/USDT",
    "timestamp": "2024-01-01T12:00:00Z",
    "indicators": {
        "rsi": 45.2,
        "sma_14": 44800.00,
        "sma_50": 44500.00,
        "ema_12": 44950.00,
        "ema_26": 44700.00,
        "macd": 250.00,
        "macd_signal": 200.00,
        "macd_histogram": 50.00,
        "bollinger_upper": 45500.00,
        "bollinger_middle": 45000.00,
        "bollinger_lower": 44500.00
    }
}
```

### 4. Wallet Management

#### 4.1 Get Wallet Balance
**GET** `/wallets/balance/`

Get current wallet balance.

**Response (200):**
```json
{
    "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    "balance": "0.125",
    "balance_usd": "5625.00",
    "unconfirmed_balance": "0.001",
    "total_received": "0.250",
    "total_sent": "0.125",
    "last_updated": "2024-01-01T12:00:00Z"
}
```

#### 4.2 Get Transaction History
**GET** `/wallets/transactions/`

Get paginated transaction history.

**Response (200):**
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/wallets/transactions/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "transaction_type": "deposit",
            "amount": "0.001",
            "txid": "abc123...",
            "status": "confirmed",
            "timestamp": "2024-01-01T12:00:00Z"
        }
    ]
}
```

#### 4.3 Create Withdrawal
**POST** `/wallets/withdraw/`

Create a withdrawal request.

**Request Body:**
```json
{
    "amount": "0.001",
    "to_address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
}
```

**Response (200):**
```json
{
    "status": "Withdrawal request submitted",
    "withdrawal_id": "W123456789",
    "amount": "0.001",
    "to_address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    "fee": "0.0001",
    "estimated_arrival": "2024-01-01T18:00:00Z"
}
```

#### 4.4 Validate Address
**POST** `/wallets/validate-address/`

Validate Bitcoin address.

**Request Body:**
```json
{
    "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
}
```

**Response (200):**
```json
{
    "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    "is_valid": true,
    "type": "bech32",
    "network": "mainnet"
}
```

### 5. Risk Management

#### 5.1 Get Risk Assessment
**GET** `/risk-management/assessment/`

Get current user's risk assessment.

**Response (200):**
```json
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
```

#### 5.2 Check Trade Risk
**POST** `/risk-management/check/`

Check risk for a potential trade.

**Request Body:**
```json
{
    "trade_type": "buy",
    "amount": 1000.00,
    "leverage": 2.0,
    "current_price": 45000.00
}
```

**Response (200):**
```json
{
    "risk_check_passed": true,
    "risk_score": 0.45,
    "position_size": 2000.00,
    "margin_required": 1000.00,
    "max_loss": 500.00,
    "warnings": [],
    "recommendations": ["Consider reducing leverage for lower risk"]
}
```

#### 5.3 Get Portfolio Risk
**GET** `/risk-management/portfolio/`

Get portfolio risk analysis.

**Response (200):**
```json
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
```

#### 5.4 Get Risk Alerts
**GET** `/risk-management/alerts/`

Get active risk alerts.

**Response (200):**
```json
[
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
```

#### 5.5 Update Risk Settings
**PUT** `/risk-management/settings/`

Update user risk settings.

**Request Body:**
```json
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
```

### 6. Compliance

#### 6.1 Check Compliance
**POST** `/compliance/check/`

Check compliance for a trade.

**Request Body:**
```json
{
    "user_id": 1,
    "trade_type": "buy",
    "amount": 1000.00,
    "source_of_funds": "salary",
    "purpose": "investment"
}
```

**Response (200):**
```json
{
    "compliance_check_passed": true,
    "aml_check": "passed",
    "kyc_status": "verified",
    "sanctions_check": "passed",
    "risk_assessment": "low",
    "warnings": [],
    "required_documents": []
}
```

#### 6.2 Get Compliance Report
**GET** `/compliance/report/`

Get compliance report.

**Query Parameters:**
- `period` (optional): Report period (daily/weekly/monthly, default: monthly)

**Response (200):**
```json
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
```

#### 6.3 Get Suspicious Activity
**GET** `/compliance/suspicious-activity/`

Get suspicious activity reports.

**Response (200):**
```json
[
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
```

### 7. WebSocket Endpoints

#### 7.1 Real-time Price Feed
**WebSocket URL:** `ws://localhost:8000/ws/price-feed/`

Subscribe to real-time price updates.

**Message Format:**
```json
{
    "type": "price_update",
    "data": {
        "symbol": "BTC/USDT",
        "price": 45000.00,
        "timestamp": "2024-01-01T12:00:00Z"
    }
}
```

#### 7.2 Trading Signals
**WebSocket URL:** `ws://localhost:8000/ws/trading-signals/`

Subscribe to real-time trading signals.

**Message Format:**
```json
{
    "type": "trading_signal",
    "data": {
        "signal": "buy",
        "confidence": 0.85,
        "indicators": {
            "rsi": 35.2,
            "sma": 44800.00
        },
        "timestamp": "2024-01-01T12:00:00Z"
    }
}
```

## Error Responses

### Common Error Codes

- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
    "error": "Error message",
    "code": "ERROR_CODE",
    "details": {
        "field": "Specific field error"
    }
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Authentication endpoints**: 5 requests per minute
- **Trading endpoints**: 10 requests per minute
- **Market data endpoints**: 60 requests per minute
- **General endpoints**: 30 requests per minute

## Trial Data

The API includes comprehensive trial data for testing:

### Sample Users
- **Email:** `demo@example.com`, **Password:** `demo123`
- **Email:** `trader@example.com`, **Password:** `trader123`
- **Email:** `admin@example.com`, **Password:** `admin123`

### Sample Trades
- 25 completed trades with various amounts and types
- Mix of buy/sell orders
- Different statuses (completed, pending, cancelled)
- Realistic P&L and ROI calculations

### Sample Market Data
- Real-time BTC/USDT price feeds
- Historical OHLCV data
- Technical indicators (RSI, SMA, EMA, MACD)
- Trading signals with confidence levels

### Sample Wallet Data
- Multiple wallet addresses
- Transaction history with deposits/withdrawals
- Balance information in BTC and USD

## Testing the API

### Using curl

```bash
# Register a new user
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'

# Login
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'

# Get profile (with token)
curl -X GET http://localhost:8000/api/accounts/profile/ \
  -H "Authorization: Bearer <your_access_token>"
```

### Using Python requests

```python
import requests

# Base URL
base_url = "http://localhost:8000/api"

# Register
response = requests.post(f"{base_url}/accounts/register/", json={
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpass123",
    "password_confirm": "testpass123"
})

# Login
response = requests.post(f"{base_url}/accounts/login/", json={
    "email": "test@example.com",
    "password": "testpass123"
})

token = response.json()['access']

# Get profile
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{base_url}/accounts/profile/", headers=headers)
print(response.json())
```

## WebSocket Testing

### Using JavaScript

```javascript
// Connect to price feed
const socket = new WebSocket('ws://localhost:8000/ws/price-feed/');

socket.onopen = function(event) {
    console.log('Connected to price feed');
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Price update:', data);
};

socket.onclose = function(event) {
    console.log('Disconnected from price feed');
};
```

## Support

For API support and questions:

- **Documentation:** http://localhost:8000/swagger/
- **ReDoc:** http://localhost:8000/redoc/
- **Email:** support@fluxor.com
- **Discord:** https://discord.gg/fluxor

## Changelog

### Version 1.0.0 (2024-01-01)
- Initial API release
- User management and authentication
- Basic trading functionality
- Real-time market data
- Risk management features
- Compliance and KYC
- WebSocket support 