# ✅ WebSocket Trade Updates & Balance Return System

## 🎯 **Complete Real-Time Trading System**

Implemented a complete real-time trading system with:
1. Backend WebSocket for live trade_sum updates
2. Backend Celery task to update trades every 5 seconds
3. Frontend WebSocket connection to receive updates
4. Balance return when trades are stopped

---

## 🔧 **Complete Implementation:**

### **1. Backend WebSocket Consumer:**
**File:** `fluxor_api/trades/consumers.py`

- ✅ **TradeUpdateConsumer** - Handles real-time connections
- ✅ **User-specific groups** - Each user gets their own channel
- ✅ **Trade update messages** - trade_sum, price, P&L updates
- ✅ **Trade completion messages** - When trade_sum = 0
- ✅ **Balance update messages** - When balance changes
- ✅ **Auto-reconnect** - Client reconnects if disconnected

### **2. Backend Celery Task:**
**File:** `fluxor_api/trades/tasks.py`

- ✅ **update_active_trades()** - Runs every 5 seconds
- ✅ **Decreases trade_sum** by 2% per interval
- ✅ **Simulates price movements** - Random ±1% changes
- ✅ **Calculates P&L** - Real-time profit/loss
- ✅ **Sends WebSocket updates** - To all connected users
- ✅ **Auto-completes trades** - When trade_sum = 0

### **3. Backend Stop Trade Endpoint:**
**File:** `fluxor_api/trades/views.py` - **StopTradeView**

- ✅ **Calculates proportional return** - Based on remaining trade_sum
- ✅ **Returns USDT to balance** - Adds back to wallet
- ✅ **Updates trade status** - Sets to 'cancelled'
- ✅ **Sends WebSocket notification** - Balance update message
- ✅ **Atomic transaction** - All-or-nothing

### **4. Frontend WebSocket Hook:**
**File:** `web/src/hooks/useTradeWebSocket.ts`

- ✅ **useTradeWebSocket()** custom hook
- ✅ **Auto-connect** on mount
- ✅ **Auto-reconnect** on disconnect
- ✅ **Message handling** - Parse and distribute updates
- ✅ **Connection status** - Track connected state
- ✅ **Error handling** - Graceful failures

### **5. Frontend Integration:**
**File:** `web/src/app/(site)/index/advanced-orders/page.tsx`

- ✅ **WebSocket connection** - Uses custom hook
- ✅ **Update handling** - Updates strategy pairs from messages
- ✅ **Stop trade API** - Calls backend when stopping
- ✅ **Balance return alert** - Shows returned amount
- ✅ **Backend trade ID** - Stores for API calls
- ✅ **Real-time sync** - Frontend matches backend state

---

## 📊 **Complete System Flow:**

### **Creating a Trade:**
```
1. User creates strategy
   ↓
2. Frontend deducts balance via API
   - POST /api/trading/deduct-balance/
   - Deducts margin + fees
   ↓
3. Backend creates Trade record
   - amount = 1.0 BTC
   - trade_sum = 1.0 BTC
   - entry_price = $50,000
   - status = 'pending'
   - is_strategy_trade = true
   ↓
4. Backend returns trade_id
   ↓
5. Frontend creates local strategy
   - Stores backend trade_id
   - Saves to localStorage
   ↓
6. User sees strategy in UI
```

### **Trading Updates (Every 5 Seconds):**
```
Backend Celery Task:
   ↓
1. Find all active trades
   - is_strategy_trade = true
   - status = 'pending'
   - trade_sum > 0
   ↓
2. For each trade:
   - Simulate price movement
   - Calculate P&L
   - Decrease trade_sum by 2%
   - Save to database
   ↓
3. Send WebSocket message:
   {
     type: 'trade_update',
     trade_id: 123,
     trade_sum: "0.98",
     current_price: "51,250",
     pnl: "625.25",
     status: "pending"
   }
   ↓
4. Frontend receives via WebSocket
   ↓
5. Updates strategy pair in state
   ↓
6. UI updates automatically
   ↓
7. User sees live changes
```

### **Trade Completion:**
```
Backend detects trade_sum = 0:
   ↓
1. Update trade status to 'executed'
   ↓
2. Send WebSocket message:
   {
     type: 'trade_completed',
     trade_id: 123,
     final_pnl: "1,250.50"
   }
   ↓
3. Frontend receives message
   ↓
4. Updates strategy status to 'completed'
   ↓
5. UI shows ✓ Completed
   ↓
6. Trading stops
```

### **Stopping a Trade:**
```
User clicks 🛑 Stop button:
   ↓
1. Frontend asks confirmation:
   "Stop this strategy? Remaining 0.75 BTC 
   will be returned to your balance."
   ↓
2. User confirms
   ↓
3. Frontend calls API:
   POST /api/trading/stop/123/
   ↓
4. Backend calculates return:
   - Initial deduction: $5,050
   - Remaining: 75% (0.75 / 1.0)
   - Amount to return: $3,787.50
   ↓
5. Backend returns balance:
   - Old balance: $4,950
   - Add: +$3,787.50
   - New balance: $8,737.50
   ↓
6. Backend updates trade:
   - status = 'cancelled'
   ↓
7. Backend sends WebSocket:
   {
     type: 'balance_update',
     balance: "8737.50",
     currency: "USDT",
     reason: "trade_stopped",
     amount_returned: "3787.50"
   }
   ↓
8. Frontend receives message
   ↓
9. Shows alert:
   "Trade stopped. $3,787.50 USDT 
   returned to your balance."
   ↓
10. Removes strategy from list
```

---

## 🌐 **WebSocket Endpoints:**

### **Connection:**
```javascript
ws://localhost:8000/ws/trades/
```

### **Message Types:**

**1. Connection Established:**
```json
{
  "type": "connection_established",
  "message": "Connected to trade updates"
}
```

**2. Trade Update:**
```json
{
  "type": "trade_update",
  "trade_id": 123,
  "trade_sum": "0.98000000",
  "current_price": "51250.50",
  "pnl": "625.25",
  "status": "pending",
  "timestamp": "2025-10-12T16:35:42Z"
}
```

**3. Trade Completed:**
```json
{
  "type": "trade_completed",
  "trade_id": 123,
  "final_pnl": "1250.50",
  "timestamp": "2025-10-12T16:40:15Z"
}
```

**4. Balance Update:**
```json
{
  "type": "balance_update",
  "balance": "8737.50",
  "currency": "USDT",
  "reason": "trade_stopped",
  "amount_returned": "3787.50",
  "timestamp": "2025-10-12T16:35:55Z"
}
```

---

## 🔧 **Celery Configuration:**

### **Beat Schedule:**
```python
app.conf.beat_schedule = {
    'update-active-trades': {
        'task': 'trades.tasks.update_active_trades',
        'schedule': 5.0,  # Every 5 seconds
    },
}
```

### **Task Execution:**
```python
@shared_task
def update_active_trades():
    active_trades = Trade.objects.filter(
        is_strategy_trade=True,
        status='pending',
        trade_sum__gt=0
    )
    
    for trade in active_trades:
        # Decrease trade_sum
        # Calculate P&L
        # Send WebSocket update
        # Auto-complete if zero
```

---

## 🔑 **Key Features:**

### **1. Real-Time Updates:**
- Backend updates trade_sum every 5 seconds
- WebSocket pushes to connected clients
- Frontend updates automatically
- No polling required

### **2. Balance Return:**
- Proportional to remaining trade_sum
- Formula: `(trade_sum / amount) × initial_deduction`
- Example: 75% remaining → 75% returned
- Instant WebSocket notification

### **3. Automatic Completion:**
- Backend detects trade_sum = 0
- Sends completion message
- Frontend marks as completed
- Trading stops automatically

### **4. State Synchronization:**
- Backend is source of truth
- Frontend syncs via WebSocket
- localStorage persists across sessions
- Reconnection recovers state

---

## 💰 **Balance Return Example:**

### **Scenario:**
```
Initial Trade:
- Amount: 1.0 BTC
- Price: $50,000
- Leverage: 10x
- Deduction: $5,050

After Some Trading:
- trade_sum: 0.75 BTC (75% remaining)
- Traded: 0.25 BTC (25%)

User Stops Trade:
- Remaining percentage: 75%
- Amount to return: $5,050 × 0.75 = $3,787.50
- Balance before: $4,950
- Balance after: $8,737.50

Result:
- User recovers 75% of initial investment
- Lost 25% (amount already traded)
```

---

## 🧪 **Testing the Complete System:**

### **Test 1: Real-Time Updates:**
```
1. Create strategy
2. Open browser dev console
3. Watch for WebSocket messages:
   "📊 Trade update received: ..."
4. See trade_sum decrease in UI
5. Verify updates every 5 seconds
```

### **Test 2: Balance Return:**
```
1. Check balance: $10,000
2. Create strategy (cost $5,050)
3. Balance: $4,950
4. Wait for some trading (e.g., trade_sum = 0.75)
5. Click 🛑 Stop
6. Confirm dialog
7. See alert: "$3,787.50 USDT returned"
8. Check balance: $8,737.50 ✅
```

### **Test 3: Automatic Completion:**
```
1. Create strategy
2. Wait for trade_sum → 0
3. Watch for WebSocket message:
   "type": "trade_completed"
4. Status changes to ✓ Completed
5. Trading stops
6. No balance return (already traded)
```

### **Test 4: WebSocket Reconnection:**
```
1. Create strategy
2. Disconnect network
3. Reconnect network
4. WebSocket auto-reconnects
5. Continues receiving updates
```

---

## ✅ **Current Status:**

### **Backend:**
- ✅ WebSocket consumer created
- ✅ Celery task scheduled (5s intervals)
- ✅ Stop trade endpoint ready
- ✅ Balance return logic implemented
- ✅ Routes configured

### **Frontend:**
- ✅ WebSocket hook created
- ✅ Connection established
- ✅ Update handling working
- ✅ Stop trade integration complete
- ✅ Balance return alerts working

### **Database:**
- ✅ trade_sum field active
- ✅ entry_price field active
- ✅ is_strategy_trade flag active
- ✅ Migration applied

---

## 🌐 **Access Your System:**

**http://localhost:5173/index/advanced-orders**

---

## 🔍 **Container Status:**
```
API:  ✅ Running (Port 8000)
Web:  ✅ Running (Port 5173)
```

---

**🎉 Complete WebSocket trade update system implemented! 🚀**

**Backend updates trade_sum every 5 seconds via Celery!**  
**Frontend receives live updates via WebSocket!**  
**Balance returned when trades are stopped!**  
**Full synchronization between backend and frontend!**
