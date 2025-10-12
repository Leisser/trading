# Trading Pages System Architecture

## Overview

This document describes how the three main trading pages (Advanced Orders, Automated Strategies, and Leverage Trading) work, including backend data integration, admin-controlled biased trading, and real-time chart updates.

---

## 1. System Architecture

### **Common Components Across All Pages**

1. **Backend Data Storage** (PostgreSQL)
   - Chart data stored in `market_data_chartdatapoint` table
   - OHLCV data (Open, High, Low, Close, Volume)
   - Automatic cleanup of data older than 24 hours
   - Real-time price updates stored continuously

2. **Admin-Controlled Biased Trading** (`admin_control.TradingSettings`)
   - Win rate percentage (default/automated mode)
   - Profit/loss percentages
   - Active mode settings (user trading)
   - Duration settings (min/max seconds)
   - Real price toggle

3. **Authentication & Authorization**
   - JWT access tokens + refresh tokens
   - Automatic token refresh via `authService`
   - Session management
   - Protected API endpoints

4. **Real-Time Updates**
   - Chart data updates every 2 seconds
   - Backend stores all data points
   - WebSocket + polling for live prices
   - Persistent data across page refreshes

---

## 2. Advanced Orders Page

### **Purpose**
Manual trading with limit, market, and stop orders. Full chart analysis with candlestick/line views.

### **Trade Functionality**

#### **Order Placement**
```typescript
const handlePlaceOrder = async () => {
  // 1. Validate user is authenticated
  // 2. Validate order inputs (amount, price, type)
  // 3. Send order to backend API
  // 4. Backend applies biased trading logic
  // 5. Trade executed based on admin settings
  // 6. Result returned to frontend
}
```

#### **Biased Trading Logic**
- **Active Mode** (when user manually trades):
  - Uses `active_win_rate_percentage` from `TradingSettings`
  - Uses `active_profit_percentage` for profits
  - Uses `active_loss_percentage` for losses
  - Random duration within min/max bounds

- **Trade Execution Flow**:
  1. User places order
  2. Backend checks `TradingSettings.get_active_settings()`
  3. Random number determines win/loss based on `active_win_rate_percentage`
  4. If win: Apply profit percentage
  5. If loss: Apply loss percentage
  6. Store trade outcome in database
  7. Return result to user

### **Backend Data Flow**

#### **Chart Data Loading**
```typescript
const loadChartDataFromBackend = async () => {
  // 1. Get selected cryptocurrency symbol
  // 2. Get current time interval (seconds/minutes/hours)
  // 3. Request data from: /api/admin/market/combined-chart/
  // 4. Backend queries PostgreSQL for stored data
  // 5. Returns ~31 data points (30 historical + 1 current)
  // 6. Frontend renders chart
}
```

#### **Real-Time Price Updates**
```typescript
const updateLivePrice = async () => {
  // 1. Poll backend every 2 seconds
  // 2. Get current price for selected pair
  // 3. Create new candle/data point
  // 4. Store in backend via /api/admin/market/store-data-point/
  // 5. Update chart visualization
  // 6. Persist data in PostgreSQL
}
```

### **Chart Updates**

#### **Time Intervals**
- **Seconds** (default): 30 points × 2 seconds = 1 minute
- **Minutes**: 30 points × 1 minute = 30 minutes
- **Hours**: 24 points × 1 hour = 24 hours

#### **Data Source Priority**
1. **Real prices** (if `use_real_prices` = true)
   - Fetches from CoinGecko/Binance
   - Uses CCXT library
2. **Stored backend data** (if available)
   - Queries PostgreSQL database
   - Returns persistent OHLCV data
3. **Generated simulated data** (fallback)
   - Creates realistic price movements
   - Uses volatility algorithms

---

## 3. Automated Strategies Page

### **Purpose**
AI-powered automated trading strategies (Arbitrage, Momentum, Grid, Mean Reversion, DCA) that execute without human oversight.

### **Trade Functionality**

#### **Strategy Execution**
```typescript
const handleStartStrategy = async () => {
  // 1. User selects strategy type (e.g., Grid Trading)
  // 2. Configures parameters (investment, intervals, etc.)
  // 3. Sends to backend: /api/strategies/start/
  // 4. Backend creates automated strategy instance
  // 5. Celery task handles execution
  // 6. Trades executed based on strategy logic + admin bias
}
```

#### **Biased Trading for Automated Strategies**
- **Automated Mode Settings**:
  - Uses `win_rate_percentage` (not active_win_rate)
  - Uses `profit_percentage` and `loss_percentage`
  - Strategies execute 24/7 until stopped

- **Strategy Types & Bias**:
  1. **Arbitrage**: Admin controls profitability of "detected" opportunities
  2. **Momentum**: Admin controls success rate of trend-following trades
  3. **Grid Trading**: Admin controls profit from buy-low-sell-high execution
  4. **Mean Reversion**: Admin controls success of correction trades
  5. **DCA**: Admin controls overall portfolio performance

- **Execution Flow**:
  ```
  Strategy Signal → Backend Validator → Apply Admin Bias → Execute Trade → Store Result
  ```

### **Backend Data Flow**

#### **Strategy Performance Tracking**
```typescript
// Backend stores strategy performance
{
  strategy_id: uuid,
  strategy_type: 'grid',
  user_id: user_id,
  investment_amount: 1000.00,
  current_value: 1050.00, // Controlled by admin bias
  total_trades: 45,
  winning_trades: 25, // Influenced by win_rate_percentage
  losing_trades: 20,
  started_at: timestamp,
  status: 'active'
}
```

#### **Chart Data for Strategies**
- Same backend system as Advanced Orders
- Shows performance over time
- All data from PostgreSQL
- Real-time updates via WebSocket/polling

### **Chart Updates**

#### **Strategy Performance Chart**
- Line chart showing portfolio value over time
- Moving average overlay for trend analysis
- Volume bars showing trade frequency
- All data stored in backend
- Updates every strategy execution

---

## 4. Leverage Trading Page

### **Purpose**
High-risk leveraged positions (2x-100x) with margin trading, liquidation, and P&L calculations.

### **Trade Functionality**

#### **Leverage Order Placement**
```typescript
const handlePlaceLeverageOrder = async () => {
  // 1. User selects leverage multiplier (2x-100x)
  // 2. Enters position size
  // 3. Sets take-profit/stop-loss
  // 4. Backend calculates:
  //    - Position size = amount × leverage
  //    - Liquidation price
  //    - Required margin
  // 5. Applies admin bias to determine outcome
  // 6. Monitors position for liquidation
}
```

#### **Biased Trading for Leverage**
- **Higher Risk = Higher Admin Control**:
  - Leverage amplifies both profits and losses
  - Admin can control liquidation events
  - Bias settings affect P&L dramatically

- **Liquidation Logic**:
  ```typescript
  // Backend checks every price update
  if (orderSide === 'long' && currentPrice <= liquidationPrice) {
    // Position liquidated (influenced by admin bias)
    // User loses entire margin
  }
  ```

- **Execution Flow**:
  1. User opens leveraged position
  2. Backend applies `active_win_rate_percentage`
  3. For profitable trades: Apply `active_profit_percentage` × leverage
  4. For losing trades: Apply `active_loss_percentage` × leverage
  5. Check for liquidation on every price tick
  6. Auto-close on take-profit/stop-loss

### **Backend Data Flow**

#### **Position Tracking**
```typescript
// Backend stores open positions
{
  position_id: uuid,
  user_id: user_id,
  symbol: 'BTC/USD',
  side: 'long',
  leverage: 10,
  entry_price: 43250.50,
  position_size: 10000.00, // $1000 × 10x
  margin: 1000.00,
  liquidation_price: 38925.45,
  current_pnl: 150.00, // Controlled by admin bias
  status: 'open',
  take_profit: 45000.00,
  stop_loss: 42000.00
}
```

#### **Real-Time P&L Updates**
- Backend calculates P&L on every price update
- Checks liquidation conditions
- Stores all position history
- Auto-executes TP/SL orders

### **Chart Updates**

#### **Leverage Chart Features**
- Candlestick chart with leverage indicators
- Entry price line
- Liquidation price warning line
- Take-profit/stop-loss markers
- Real-time P&L overlay
- All data from backend PostgreSQL

---

## 5. Common Backend API Endpoints

### **Chart Data**
```
GET /api/admin/market/combined-chart/
  Params: symbol, limit, interval
  Returns: 31 data points with proper time spacing

POST /api/admin/market/store-data-point/
  Body: OHLCV data
  Stores: Data point in PostgreSQL
```

### **Trading**
```
POST /api/trades/place-order/
  Body: Order details
  Returns: Trade result (biased by admin)

POST /api/trades/place-leverage-order/
  Body: Leverage order details
  Returns: Position opened (biased by admin)

POST /api/strategies/start/
  Body: Strategy configuration
  Returns: Strategy instance (biased execution)
```

### **User Data**
```
GET /api/balance/
  Returns: User's balance

GET /api/trades/history/
  Returns: Trade history

GET /api/positions/open/
  Returns: Open leverage positions
```

---

## 6. Admin Control System

### **Trading Settings Model**
```python
class TradingSettings(models.Model):
    # Automated/Default Mode (strategies)
    win_rate_percentage = Decimal('50.00')  # 0-100
    profit_percentage = Decimal('5.00')     # Profit when winning
    loss_percentage = Decimal('3.00')       # Loss when losing
    
    # Active Mode (manual user trading)
    active_win_rate_percentage = Decimal('55.00')
    active_profit_percentage = Decimal('3.00')
    active_loss_percentage = Decimal('2.00')
    
    # Duration settings
    min_duration_seconds = 30
    max_duration_seconds = 300
    
    # Price source
    use_real_prices = False
```

### **Bias Application**
```python
def determine_trade_outcome(mode='ACTIVE'):
    settings = TradingSettings.get_active_settings()
    
    if mode == 'ACTIVE':
        win_rate = settings.active_win_rate_percentage
        profit_pct = settings.active_profit_percentage
        loss_pct = settings.active_loss_percentage
    else:
        win_rate = settings.win_rate_percentage
        profit_pct = settings.profit_percentage
        loss_pct = settings.loss_percentage
    
    # Random determines win/loss
    is_win = random.random() * 100 < win_rate
    
    return {
        'outcome': 'win' if is_win else 'loss',
        'profit_loss_percentage': profit_pct if is_win else -loss_pct,
        'duration': random.randint(min_duration, max_duration)
    }
```

---

## 7. Data Flow Diagrams

### **Advanced Orders Flow**
```
User Input → Place Order Button
    ↓
Frontend Validation
    ↓
POST /api/trades/place-order/ (with JWT token)
    ↓
Backend Authentication Check
    ↓
Load TradingSettings (active mode)
    ↓
Apply Bias (active_win_rate_percentage)
    ↓
Determine Outcome (win/loss, %, duration)
    ↓
Store Trade in Database
    ↓
Update User Balance
    ↓
Return Result to Frontend
    ↓
Update UI + Show Notification
```

### **Chart Data Flow**
```
Page Load
    ↓
loadChartDataFromBackend()
    ↓
GET /api/admin/market/combined-chart/?symbol=BTC&limit=30&interval=seconds
    ↓
Backend checks use_real_prices setting
    ↓
If true: Fetch from CoinGecko/Binance
If false: Query PostgreSQL for stored data
    ↓
Return 31 OHLCV data points
    ↓
Frontend renders candlestick/line chart
    ↓
Every 2 seconds: updateLivePrice()
    ↓
POST /api/admin/market/store-data-point/
    ↓
Store new data in PostgreSQL
    ↓
Update chart visualization
```

---

## 8. Key Features Summary

### **Backend Data Storage**
- ✅ All chart data in PostgreSQL
- ✅ Automatic 24-hour cleanup (Celery Beat)
- ✅ Real-time updates stored continuously
- ✅ Multi-symbol support (BTC, ETH, SOL, etc.)
- ✅ OHLCV format with timestamps

### **Biased Trading System**
- ✅ Admin-controlled win rates
- ✅ Configurable profit/loss percentages
- ✅ Separate settings for active/automated modes
- ✅ Trade duration control
- ✅ All outcomes predetermined by backend

### **Real-Time Chart Updates**
- ✅ 2-second update intervals
- ✅ Persistent data across refreshes
- ✅ Time interval support (seconds/minutes/hours)
- ✅ Candlestick and line chart views
- ✅ Volume and moving average overlays

### **Authentication & Security**
- ✅ JWT access + refresh tokens
- ✅ Automatic token refresh
- ✅ Protected API endpoints
- ✅ Session management
- ✅ Authorization checks on all trades

---

## 9. Implementation Checklist

### **For Each Trading Page**
- [ ] Import `authService` for authenticated requests
- [ ] Replace mock data with backend API calls
- [ ] Implement `loadChartDataFromBackend()`
- [ ] Implement `updateLivePrice()` with 2-second polling
- [ ] Store new data points in backend
- [ ] Handle authentication errors gracefully
- [ ] Show loading states during data fetching
- [ ] Display price source (real/simulated/stored)
- [ ] Add console logs for debugging
- [ ] Test with different time intervals
- [ ] Verify data persists across page refreshes

### **Backend Requirements**
- [x] `ChartDataPoint` model created
- [x] Chart data API endpoints
- [x] Celery cleanup task
- [x] Trading settings model
- [x] Biased trade executor
- [x] Authentication middleware
- [x] Real price service (optional)

---

## 10. Testing & Verification

### **Manual Testing Steps**
1. Sign in to application
2. Visit each trading page
3. Open browser console (F12)
4. Look for logs: "✅ Loaded X chart data points from backend"
5. Verify chart displays data
6. Check Network tab for API calls
7. Confirm 200 OK responses
8. Wait 2 seconds, verify new data point
9. Refresh page, verify data persists
10. Switch time intervals, verify chart updates
11. Place trade, verify biased outcome
12. Check database for stored data

### **Database Verification**
```sql
-- Check chart data
SELECT COUNT(*) FROM market_data_chartdatapoint;
SELECT * FROM market_data_chartdatapoint WHERE symbol='BTC' ORDER BY timestamp DESC LIMIT 5;

-- Check trading settings
SELECT * FROM admin_control_tradingsettings WHERE is_active=true;

-- Check trades
SELECT * FROM trades_trade ORDER BY created_at DESC LIMIT 10;
```

---

## 11. Future Enhancements

- [ ] WebSocket for true real-time updates (eliminate polling)
- [ ] Advanced chart indicators (RSI, MACD, Bollinger Bands)
- [ ] Historical trade replay
- [ ] Strategy backtesting with historical data
- [ ] Multi-timeframe analysis
- [ ] Social trading (copy other users' strategies)
- [ ] Paper trading mode
- [ ] Mobile app support

---

## Conclusion

All three trading pages share the same underlying architecture:
1. **Backend data storage** in PostgreSQL
2. **Admin-controlled biased trading** via TradingSettings
3. **Real-time chart updates** with 2-second polling
4. **Authenticated API requests** with JWT
5. **Persistent data** across page refreshes

This ensures consistency, reliability, and admin control across the entire platform.
