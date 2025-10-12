# Real Trading System - How It Works

## ✅ **The System IS Real Trading**

The trading system is **NOT simulated** - it performs **real trade execution** with:
- ✅ Real balance deductions from user wallets
- ✅ Real cryptocurrency balance updates
- ✅ Real trade records stored in PostgreSQL
- ✅ Real P&L calculations
- ✅ Real trading fees (0.1% for trades, 0.3% for swaps)
- ✅ Real transaction atomicity (database commits)

---

## 🔧 **How Real Trading Works**

### **Trade Execution Flow**

```
User Places Trade
    ↓
Backend receives POST /api/trading/execute/
    ↓
BiasedTradeExecutor.execute_biased_buy_order()
    ↓
TradeExecutor.execute_buy_order()  ← REAL EXECUTION
    ↓
1. Validates cryptocurrency exists
2. Calculates total cost with leverage
3. Checks user has sufficient USDT balance
4. Deducts USDT from wallet (REAL DEDUCTION)
5. Adds cryptocurrency to wallet (REAL ADDITION)
6. Calculates trading fees (0.1%)
7. Creates Trade record in PostgreSQL
8. Commits database transaction
    ↓
BiasedTradeExecutor determines outcome
    ↓
Creates UserTradeOutcome record
    ↓
Stores: expected outcome, percentage, duration, target close time
    ↓
Returns trade + outcome to frontend
    ↓
User sees result with balance updated
```

---

## 💾 **What Gets Stored in Database**

### **1. Trade Record** (`trades_trade` table)
```python
Trade.objects.create(
    user=user,                        # Who made the trade
    cryptocurrency=cryptocurrency,     # What crypto (BTC, ETH, etc.)
    trade_type='buy',                 # buy, sell, or swap
    amount=100,                       # How much crypto
    price=43250.50,                   # Price per unit
    total_value=4325050.00,           # Total trade value
    leverage=10,                      # Leverage multiplier
    status='executed',                # Trade executed
    pnl=0,                           # Profit/Loss (calculated on sell)
    fees=4325.05,                    # Trading fees (0.1%)
    executed_at=timezone.now()       # When executed
)
```

### **2. User Trade Outcome** (`admin_control_usertradeoutcome` table)
```python
UserTradeOutcome.objects.create(
    user=user,
    trade=trade,
    outcome='win',                    # Admin-determined outcome
    outcome_percentage=3.0,           # Profit percentage
    duration_seconds=127,             # How long until close
    target_close_time=future_time,    # When to auto-close
    is_executed=False                 # Not closed yet
)
```

### **3. Wallet Balances** (`wallets_cryptobalance` table)
```python
# Before trade:
USDT Balance: 10000.00
BTC Balance: 0

# After buy trade:
USDT Balance: 9000.00   # Deducted 1000 USDT
BTC Balance: 0.0231     # Added BTC (1000/43250.50)

# After sell trade (win):
USDT Balance: 10030.00  # Got back 1000 + 30 profit - fees
BTC Balance: 0          # Sold all BTC
```

### **4. Chart Data** (`market_data_chartdatapoint` table)
```python
ChartDataPoint.objects.create(
    symbol='BTC',
    timestamp=timezone.now(),
    open_price=43250.50,
    high_price=43280.75,
    low_price=43240.20,
    close_price=43270.30,
    volume=450000,
    source='simulated' or 'real',
    created_at=timezone.now()
)
```

---

## 🎯 **Real vs. Simulated**

### **What's REAL:**
- ✅ **Balance deductions** - Actually removes USDT from wallet
- ✅ **Balance additions** - Actually adds crypto to wallet
- ✅ **Trade records** - Stored permanently in PostgreSQL
- ✅ **P&L calculations** - Real profit/loss tracking
- ✅ **Trading fees** - Actually deducted (0.1%)
- ✅ **Database transactions** - Atomic commits
- ✅ **Trade history** - All trades stored forever
- ✅ **Multi-currency wallet** - Real crypto balances

### **What's "Biased" (Admin-Controlled):**
- ⚖️ **Win/Loss determination** - Admin sets win rate percentage
- ⚖️ **Profit/Loss percentage** - Admin sets profit/loss amounts
- ⚖️ **Trade duration** - Admin sets how long until auto-close
- ⚖️ **Price source** - Can use real or simulated prices

### **What's Simulated (Optional):**
- 🔄 **Price data** - Can use simulated OR real prices (toggle via admin)
- 🔄 **Market movements** - Generated if real prices not enabled

---

## 💡 **How to Verify Real Trading**

### **Test 1: Check Database**
```bash
# View all trades
docker exec trading-db-1 psql -U fluxor -d fluxor -c \
  "SELECT id, user_id, cryptocurrency_id, trade_type, amount, price, pnl, fees, status, executed_at FROM trades_trade ORDER BY executed_at DESC LIMIT 10;"

# View wallet balances
docker exec trading-db-1 psql -U fluxor -d fluxor -c \
  "SELECT w.user_id, c.symbol, cb.balance FROM wallets_cryptobalance cb JOIN wallets_multicurrencywallet w ON cb.wallet_id = w.id JOIN trades_cryptocurrency c ON cb.cryptocurrency_id = c.id;"

# View trade outcomes
docker exec trading-db-1 psql -U fluxor -d fluxor -c \
  "SELECT user_id, trade_id, outcome, outcome_percentage, duration_seconds, target_close_time, is_executed FROM admin_control_usertradeoutcome ORDER BY created_at DESC LIMIT 10;"
```

### **Test 2: Execute a Trade**
```
1. Sign in
2. Check initial balance: $10,000
3. Place $100 buy order
4. Check balance: Should be $9,900 (deducted!)
5. Check database for trade record
6. Wait for duration to complete
7. Trade auto-closes
8. Check balance: $10,030 (if win with 3% profit)
9. Database shows:
   - Buy trade record
   - Sell trade record
   - UserTradeOutcome record
   - Balance changes in wallets
```

### **Test 3: Balance Verification**
```bash
# Before trade
docker exec trading-api-1 python manage.py shell -c "
from wallets.models import MultiCurrencyWallet, CryptoBalance
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(email='admin@fluxor.pro')
wallet = MultiCurrencyWallet.objects.get(user=user)
balances = CryptoBalance.objects.filter(wallet=wallet)
for b in balances:
    print(f'{b.cryptocurrency.symbol}: {b.balance}')
"

# Execute trade via frontend

# After trade
docker exec trading-api-1 python manage.py shell -c "
from wallets.models import MultiCurrencyWallet, CryptoBalance
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(email='admin@fluxor.pro')
wallet = MultiCurrencyWallet.objects.get(user=user)
balances = CryptoBalance.objects.filter(wallet=wallet)
for b in balances:
    print(f'{b.cryptocurrency.symbol}: {b.balance}')
"

# Balances should be DIFFERENT (proves real trading!)
```

---

## 📊 **Chart Data Storage**

Chart data is also REAL and stored:

```
Every 2 seconds (or 1 minute/hour):
1. Frontend polls: GET /api/admin/market/price-auto/?symbol=BTC
2. Creates new OHLC candle
3. Stores: POST /api/admin/market/store-data-point/
4. Backend saves to: market_data_chartdatapoint table
5. Data persists for 24 hours
6. Celery cleanup task removes old data
```

**Database Query:**
```bash
docker exec trading-db-1 psql -U fluxor -d fluxor -c \
  "SELECT symbol, timestamp, close_price, source FROM market_data_chartdatapoint ORDER BY timestamp DESC LIMIT 10;"
```

---

## 🎯 **Key Points**

### **The System is REAL:**
1. **Real database transactions** - Balances actually change
2. **Real trade records** - Stored permanently
3. **Real P&L tracking** - Calculated and stored
4. **Real fees** - Deducted from proceeds
5. **Real wallet management** - Multi-currency balances

### **Admin "Bias" Controls Outcomes:**
- Admin doesn't fake trades
- Admin controls the **probability** of winning
- Admin controls the **percentage** of profit/loss
- The trade execution itself is 100% real

### **Think of it like a casino:**
- **Real money** moves (balances change)
- **Real records** kept (trades stored)
- **House edge** controlled (win rate biased)
- **Payouts** predetermined (profit % set)

---

## ✅ **Conclusion**

The trading system is **NOT simulated** - it's **REAL** with:
- ✅ Real balance management
- ✅ Real trade execution
- ✅ Real database storage
- ✅ Real P&L calculations
- ✅ Admin-controlled outcomes (bias)

The only "simulated" part is the **price data source** (can toggle to use real prices from CoinGecko/Binance).

**Everything else is 100% real trading with real database storage!** 🚀
