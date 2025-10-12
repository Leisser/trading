# Activity-Based Trading System

## Overview

The trading system now operates in two automatic modes based on user activity:

### 🟢 **IDLE MODE** (No Active Trading)
- **When**: No trades in the last 10 minutes
- **Result**: Users ALWAYS WIN
- **Profit**: 5% (default, configurable)
- **Duration**: 30 minutes (default, configurable)

### 🔴 **ACTIVE MODE** (Users Trading)
- **When**: Any user places a trade
- **Result**: Users ALWAYS LOSE
- **Loss**: 80% (default, configurable)
- **Duration**: 5 minutes (default, configurable)

## How It Works

### Automatic Mode Switching

```
System constantly checks:
├─ Any trades in last 10 minutes?
│  ├─ NO  → IDLE MODE (profits)
│  └─ YES → ACTIVE MODE (losses)
```

### Trade Execution Flow

**Scenario 1: IDLE MODE**
```
1. User places buy order for 0.1 BTC @ $43,250
2. System checks: No recent trades
3. Mode: IDLE
4. Outcome: WIN +5% profit
5. Duration: 30 minutes
6. After 30 minutes: Auto-sells at $45,412.50 (+5%)
7. User gains: +$216.25
```

**Scenario 2: ACTIVE MODE**
```
1. User places buy order for 0.1 BTC @ $43,250
2. System checks: Someone traded 5 minutes ago
3. Mode: ACTIVE
4. Outcome: LOSS -80% loss
5. Duration: 5 minutes
6. After 5 minutes: Auto-sells at $8,650 (-80%)
7. User loses: -$3,460
```

## Admin Control Panel (Board Page)

### Trading Control Card

New card in the Board page displays:

- **Current Mode**: 🟢 IDLE or 🔴 ACTIVE
- **Idle Settings**: +5% profit every 30 min
- **Active Settings**: -80% loss every 5 min
- **Configure Button**: Opens settings modal
- **Set to Default Button**: Resets to defaults

### Trading Settings Modal

Click "Configure" to open modal with:

**Idle Mode Settings:**
- Profit Percentage (%)
- Duration (minutes)

**Active Mode Settings:**
- Loss Percentage (%)
- Duration (minutes)

**Action Buttons:**
- Save Settings
- Set to Default
- Cancel

### Default Settings

Click "Set to Default" to reset to:
```
Idle Mode:
  - Profit: 5%
  - Duration: 30 minutes

Active Mode:
  - Loss: 80%
  - Duration: 5 minutes
```

## API Endpoints

### Get Trading Mode Status
```bash
GET /api/admin/settings/mode-status/
```

Response:
```json
{
  "is_user_trading": false,
  "current_mode": "idle",
  "current_outcome": "win",
  "current_percentage": 5.0,
  "current_duration": 1800,
  "settings": {...}
}
```

### Update Activity-Based Settings
```bash
POST /api/admin/settings/activity-based/
{
  "idle_profit_percentage": 5.0,
  "idle_duration_seconds": 1800,
  "active_loss_percentage": 80.0,
  "active_duration_seconds": 300
}
```

### Set to Default
```bash
POST /api/admin/settings/default/
```

Resets to default values automatically.

## Automated Background Tasks

### Celery Beat Schedule

**Task 1: auto_close_due_trades**
- **Frequency**: Every 60 seconds
- **Purpose**: Close trades that reached target time
- **Action**: Applies win/loss based on predetermined outcome

**Task 2**: cleanup_old_market_data
- **Frequency**: Daily at midnight
- **Purpose**: Remove old market data
- **Action**: Keeps last 24 hours only

### How Auto-Close Works

```python
Every 60 seconds:
  1. Find all trades where target_close_time <= now
  2. For each trade:
     a. Get predetermined outcome (win/loss)
     b. Calculate exit price
     c. Execute sell order
     d. Update user balance
     e. Record profit/loss
```

## Real-Time WebSocket Integration

### Market Data Streaming

**WebSocket URL**: `ws://localhost:8000/ws/market/BTC/`

**Updates**: Every 5 seconds (configurable)

**Data Format**:
```json
{
  "type": "market_update",
  "symbol": "BTC",
  "timestamp": "2025-10-11T08:00:00Z",
  "price": 43250.50,
  "open": 43180.20,
  "high": 43300.00,
  "low": 43150.00,
  "close": 43250.50,
  "volume": 567890.12,
  "change_24h": 2.45
}
```

### Frontend Integration

All Index trading pages now have:
- ✅ Live WebSocket connection
- ✅ Real-time chart updates
- ✅ Connection status indicator (green pulse = connected)
- ✅ Auto-reconnection on disconnect

## User Experience

### What Users See:

**Trading Interface:**
- Live price charts (candlestick & line)
- Real-time price updates
- Trade execution forms
- Balance validation
- Profit/loss results

**After Trade:**
- Trade confirmation
- Expected outcome (shown for transparency in response)
- Fees charged
- Updated balance

### What Users Don't See:

- Predetermined win/loss outcome
- Exact close time
- Activity mode detection
- Admin settings

## Admin Dashboard

### Board Page Features:

1. **Trading Control Card**
   - Shows current mode (Idle/Active)
   - Displays current settings
   - Quick access to configure
   - One-click default reset

2. **Trading Settings Modal**
   - Adjust idle profit %
   - Adjust idle duration
   - Adjust active loss %
   - Adjust active duration
   - Save or reset to defaults

3. **Real-Time Mode Display**
   - Green (Idle) = Users winning
   - Red (Active) = Users losing
   - Updates based on recent activity

## Configuration Examples

### Example 1: Slow Drain (Current Default)
```
Idle:   +5% every 30 minutes
Active: -80% every 5 minutes

Effect: When users trade, they lose fast.
        When idle, they gain slowly.
```

### Example 2: Fast Drain
```
Idle:   +2% every 60 minutes
Active: -90% every 2 minutes

Effect: Users lose even faster when active.
```

### Example 3: Gentle Mode
```
Idle:   +10% every 30 minutes
Active: -20% every 15 minutes

Effect: Users can actually win sometimes.
```

### Example 4: Casino Mode
```
Idle:   +1% every 120 minutes
Active: -95% every 1 minute

Effect: Maximum loss, minimal gain.
```

## Database Models

### TradingSettings Fields:

```python
# Activity-Based Settings
idle_profit_percentage = 5.00          # Profit when idle
idle_duration_seconds = 1800           # 30 minutes

active_loss_percentage = 80.00         # Loss when active
active_duration_seconds = 300          # 5 minutes

# Market Simulation
price_volatility_percentage = 2.00     # ±2% price changes
update_interval_seconds = 5            # WebSocket update rate
```

### UserTradeOutcome Fields:

```python
user                  # Who placed the trade
trade                 # Link to Trade model
outcome               # 'win' or 'loss'
outcome_percentage    # Profit or loss %
duration_seconds      # How long until close
target_close_time     # When to close
is_executed           # Has it closed?
executed_at           # When it closed
```

## Testing the System

### 1. Set Up Admin Settings (Board Page)

1. Login as superuser
2. Go to Board page
3. See "Trading Control" card
4. Current mode shows: IDLE (no recent trades)
5. Click "Configure"
6. Set your preferences or use defaults
7. Click "Save Settings"

### 2. Place a Trade (User)

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

Response includes:
```json
{
  "success": true,
  "outcome": {
    "expected_outcome": "loss",
    "expected_percentage": 80.0,
    "target_close_time": "2025-10-11T08:05:00Z",
    "duration_seconds": 300
  }
}
```

### 3. Check Mode Changed

Now mode switches to ACTIVE because a trade was placed.

### 4. Wait for Auto-Close

After 5 minutes:
- Celery task runs
- Auto-sells BTC at -80% price
- User loses 80%
- Balance updated

### 5. Return to Idle

10 minutes after last trade:
- Mode switches back to IDLE
- Next trade will be +5% profit

## Files Created/Modified

### Backend:
1. ✅ `fluxor_api/admin_control/models.py` - Added activity-based fields
2. ✅ `fluxor_api/trades/biased_trade_executor.py` - Activity-based logic
3. ✅ `fluxor_api/admin_control/views.py` - New admin endpoints
4. ✅ `fluxor_api/admin_control/urls.py` - New routes
5. ✅ `fluxor_api/admin_control/serializers.py` - Serializers
6. ✅ `fluxor_api/admin_control/admin.py` - Admin interface
7. ✅ `fluxor_api/trades/tasks.py` - Celery auto-close task
8. ✅ `fluxor_api/fluxor_api/celery.py` - Beat schedule
9. ✅ `fluxor_api/core/market_consumer.py` - WebSocket consumer
10. ✅ `fluxor_api/core/routing.py` - WebSocket routing

### Frontend:
11. ✅ `web/src/hooks/useMarketWebSocket.ts` - WebSocket hook
12. ✅ `web/src/app/(site)/board/page.tsx` - Trading Control UI
13. ✅ `web/src/app/(site)/index/advanced-orders/page.tsx` - Live data integration

### Documentation:
14. ✅ `ACTIVITY_BASED_TRADING.md` - This file
15. ✅ `BIASED_TRADING_SYSTEM.md` - Complete system guide
16. ✅ `TRADE_EXECUTION_API.md` - API documentation

## Key Features Summary

✅ **Activity Detection**: Checks for trades in last 10 minutes
✅ **Automatic Switching**: Idle ↔ Active based on activity
✅ **Always Winning (Idle)**: 5% profit every 30 min when no trading
✅ **Always Losing (Active)**: 80% loss every 5 min when trading
✅ **Admin Control**: Full control from Board page
✅ **Set to Default**: One-click reset button
✅ **Real-Time WebSocket**: Live charts and data
✅ **Auto-Close Trades**: Celery handles everything
✅ **Balance Validation**: Users can only trade what they have
✅ **Profit/Loss Tracking**: Automatic P/L calculation

## Important Notes

⚠️ **Activity Trigger**: Just ONE trade in 10 minutes triggers ACTIVE mode
⚠️ **Immediate Effect**: Mode change affects ALL new trades
⚠️ **Celery Timing**: Trades close within 60 seconds of target time
⚠️ **Default Values**: Can be changed anytime from Board page
⚠️ **No User Notification**: Users don't see mode status

## Monitoring

Check current mode:
```bash
GET /api/admin/settings/mode-status/
```

View active positions:
```bash
GET /api/admin/outcomes/active/
```

Monitor Celery tasks:
```bash
docker-compose logs celery_beat --tail=20
```

---

The system is now fully operational with activity-based trading! 🎰💰

