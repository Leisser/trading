# How Updates Are Handled - Complete Flow

## Overview

This document explains how the system handles price updates, data flow, and how changes propagate from backend to frontend.

---

## 🔄 Update Flow Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     UPDATE SOURCES                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Real Exchanges (CCXT/CoinGecko)                         │
│     ├─ Binance API (Primary)                                │
│     └─ CoinGecko API (Fallback)                             │
│                                                              │
│  2. Simulated Prices                                        │
│     ├─ Price Simulator (For Active Trades)                  │
│     └─ Database Values (Default)                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   BACKEND PROCESSING                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  RealPriceService.get_current_price()                       │
│     ↓                                                        │
│  Cache Check (60s TTL)                                      │
│     ↓                                                        │
│  Try: CCXT → CoinGecko → Database                           │
│     ↓                                                        │
│  Response: { price, source, timestamp }                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                      API ENDPOINTS                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  GET /api/admin/market/price-auto/                          │
│     ├─ Checks: use_real_prices setting                      │
│     ├─ If TRUE  → Fetch real price                          │
│     └─ If FALSE → Fetch simulated price                     │
│                                                              │
│  GET /api/admin/market/real-price/                          │
│     └─ Always fetches real (requires toggle ON)             │
│                                                              │
│  GET /api/admin/market/current-price/                       │
│     └─ Returns simulated prices (legacy)                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   FRONTEND POLLING                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  useEffect(() => {                                           │
│    const interval = setInterval(() => {                     │
│      updateLivePrice();  // Calls API every 2 seconds       │
│    }, 2000);                                                 │
│  }, [selectedPair]);                                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                    STATE UPDATES                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. setPriceSource(data.source)      // 'real' or 'simulated'│
│  2. setLastUpdateTime(now)           // Current timestamp    │
│  3. setPriceFlash(true)              // Trigger animation    │
│  4. setNewDataAnimation(true)        // Chart highlight      │
│  5. setChartData([...prev, new])     // Add to chart         │
│  6. setSelectedPair({...price})      // Update current price │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                     UI UPDATES                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Price Display Flashes (500ms)                           │
│  2. Chart Adds New Candle/Point                             │
│  3. New Data Highlight Animation (1000ms)                   │
│  4. Last Update Time Shows                                  │
│  5. Price Source Badge Shows ("Real Prices" or "Simulated") │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📋 Detailed Update Steps

### 1. Admin Enables Real Prices

**Action**: Admin toggles "Use Real Prices" in board settings

**What Happens**:
```
User clicks toggle → 
Frontend sends PATCH request → 
Backend updates TradingSettings.use_real_prices = True → 
Database saved → 
Response: Success
```

**File**: `web/src/app/(site)/board/page.tsx`
```typescript
// Save to backend
const response = await fetch('/api/admin/settings/activity-based/', {
  method: 'POST',
  body: JSON.stringify({
    use_real_prices: useRealPrices  // Boolean: true/false
  })
});
```

### 2. Frontend Requests Price Update

**Trigger**: Every 2 seconds (configurable)

**What Happens**:
```
Timer fires (2s) →
updateLivePrice() called →
Fetch /api/admin/market/price-auto/ →
Waits for response
```

**File**: `web/src/app/(site)/index/advanced-orders/page.tsx`
```typescript
useEffect(() => {
  const interval = setInterval(() => {
    updateLivePrice();  // Called every 2 seconds
  }, 2000);
  
  return () => clearInterval(interval);
}, [selectedPair]);
```

### 3. Backend Determines Price Source

**Decision Logic**:
```
GET /api/admin/market/price-auto/?symbol=BTC

↓

if (settings.use_real_prices == TRUE):
    → Call RealPriceService.get_current_price('BTC')
    → Return: { price: 110374.59, source: 'real' }
else:
    → Get from Database/Simulator
    → Return: { price: 43250.00, source: 'simulated' }
```

**File**: `fluxor_api/admin_control/market_data_views.py`
```python
def get_price_auto(request):
    settings = TradingSettings.get_active_settings()
    
    if settings.use_real_prices:
        price_service = get_price_service()
        price = price_service.get_current_price(symbol)
        return Response({
            'price': price,
            'source': 'real'  # ← Important!
        })
    else:
        crypto = Cryptocurrency.objects.get(symbol=symbol)
        return Response({
            'price': float(crypto.current_price),
            'source': 'simulated'  # ← Important!
        })
```

### 4. Real Price Service Fetches Data

**When Real Prices Are Enabled**:

```
get_current_price('BTC') called

↓ Check Cache
cache.get('real_price_BTC')
  → If found (< 60s old): Return cached value
  → If not found: Continue

↓ Try CCXT (Binance)
exchange.fetch_ticker('BTC/USDT')
  → Success: Return price, cache it
  → Fail: Continue to fallback

↓ Try CoinGecko
cg.get_price(ids='bitcoin', vs_currencies='usd')
  → Success: Return price, cache it
  → Fail: Return None

↓ Final Fallback
Return None → API returns error or database value
```

**File**: `fluxor_api/admin_control/real_price_service.py`
```python
def get_current_price(self, symbol='BTC'):
    # 1. Check cache
    cached = cache.get(f'real_price_{symbol}')
    if cached:
        return float(cached)
    
    # 2. Try CCXT
    try:
        ticker = self.exchange.fetch_ticker(f'{symbol}/USDT')
        price = float(ticker['last'])
        cache.set(f'real_price_{symbol}', price, 60)
        return price
    except:
        pass
    
    # 3. Try CoinGecko
    try:
        data = self.cg.get_price(ids='bitcoin', vs_currencies='usd')
        price = float(data['bitcoin']['usd'])
        cache.set(f'real_price_{symbol}', price, 60)
        return price
    except:
        pass
    
    return None
```

### 5. Frontend Receives and Processes Update

**Response Received**:
```json
{
  "symbol": "BTC",
  "price": 110374.59,
  "timestamp": "2025-10-11T18:45:23Z",
  "source": "real"
}
```

**Frontend Processing**:
```typescript
const data = await response.json();

// 1. Log the update
console.log('📊 Backend price data:', data);
console.log('🌐 Price source:', data.source.toUpperCase());

// 2. Update price source badge
setPriceSource(data.source);  // 'real' or 'simulated'

// 3. Update timestamp
setLastUpdateTime(now.toLocaleTimeString());

// 4. Trigger animations
setPriceFlash(true);          // Price number flashes
setNewDataAnimation(true);    // Chart highlights new data

// 5. Add to chart data
const newCandle = {
  timestamp: data.timestamp,
  open: lastCandle.close,
  close: data.price,
  high: Math.max(lastCandle.close, data.price) * 1.003,
  low: Math.min(lastCandle.close, data.price) * 0.997,
  volume: Math.random() * 500000
};
setChartData(prev => [...prev.slice(-29), newCandle]);

// 6. Update current price display
setSelectedPair(prev => ({
  ...prev,
  current_price: data.price
}));
```

### 6. UI Renders Updates

**Visual Changes**:
1. **Price number** flashes white → primary color (500ms)
2. **Chart** adds new candle/point on the right
3. **New data highlight** appears (blue glow, 1000ms)
4. **Pulse animation** on newest point (1000ms)
5. **"Last update" timestamp** updates
6. **Source badge** shows "Real Prices" (blue) or "Simulated" (yellow)

---

## ⚙️ Configuration: How Updates Change

### Scenario A: Admin Enables Real Prices

**Before**:
```
Timer (2s) → /price-auto/ → Database → { price: 43250, source: 'simulated' }
           → Frontend updates with simulated prices
```

**After** (Admin toggles ON):
```
Timer (2s) → /price-auto/ → CCXT/CoinGecko → { price: 110374.59, source: 'real' }
           → Frontend updates with REAL prices
           → Badge changes to "Real Prices" (blue)
```

**What Changed**: Just the backend data source! Frontend code unchanged.

### Scenario B: Admin Changes Update Interval

**Current**: Updates every 2 seconds
```typescript
setInterval(() => updateLivePrice(), 2000);
```

**To Change**: Modify interval in advanced-orders page
```typescript
// For faster updates (1 second)
setInterval(() => updateLivePrice(), 1000);

// For slower updates (5 seconds)
setInterval(() => updateLivePrice(), 5000);
```

### Scenario C: Admin Changes Active Mode Settings

**Action**: Admin changes `active_win_rate_percentage` from 20% to 50%

**Update Flow**:
```
1. Admin saves in board → Database updated immediately
2. Next trade placed → BiasedTradeExecutor reads new settings
3. Random chance: 0-100, if ≤ 50 → WIN, if > 50 → LOSS
4. Trade outcome determined → Stored in UserTradeOutcome
5. Price simulator generates path to target
6. Frontend polls for updates → Gets simulated prices following path
```

**Result**: Next trade has 50% chance of profit (was 20%)

---

## 🔌 How Code Updates Are Deployed

### Backend Changes (Python/Django)

**Process**:
```bash
# 1. Make code changes
edit fluxor_api/admin_control/models.py

# 2. Create migration (if model changed)
docker exec trading-api-1 python manage.py makemigrations

# 3. Apply migration
docker exec trading-api-1 python manage.py migrate

# 4. Restart container to load new code
docker restart trading-api-1
```

**Files Affected**:
- Python code: Auto-reloaded in development mode
- Models: Require migration + restart
- Views/Logic: Require restart only

### Frontend Changes (React/Next.js)

**Development Mode (with hot reload)**:
```
1. Edit file: web/src/app/(site)/board/page.tsx
2. Save file
3. Next.js detects change
4. Auto-reloads in browser (if using npm run dev)
```

**Production Mode (Docker)**:
```bash
# 1. Make code changes
edit web/src/app/(site)/board/page.tsx

# 2. Rebuild container
docker-compose up -d --build web

# 3. Hard refresh browser
Cmd/Ctrl + Shift + R
```

### Current Setup (Docker Volumes)

**Development**:
```yaml
web:
  volumes:
    - ./web:/app          # Code mounted as volume
    - /app/node_modules   # Persistent node_modules
    - /app/.next          # Persistent build cache
```

**What This Means**:
- Code changes in `/web` are reflected in container
- But Next.js needs rebuild to see changes
- Use `docker restart` or `docker-compose up -d --build web`

---

## 🎯 Current Update Timings

| Component | Update Frequency | Method |
|-----------|-----------------|---------|
| **Price Data** | Every 2 seconds | HTTP polling |
| **Chart Data** | Every 2 seconds | Added with price update |
| **WebSocket** | Real-time | WebSocket (if configured) |
| **Real Price Cache** | 60 seconds | Redis/Django cache |
| **CCXT API** | On-demand | No rate limit (public) |
| **CoinGecko** | On-demand | 50/min rate limit |

---

## 📊 Update Sequence Diagram

### When Real Prices Are Enabled:

```
Frontend                Backend             CCXT/CoinGecko        Cache
   │                       │                      │                │
   │──updateLivePrice()───→│                      │                │
   │                       │──Check cache────────→│                │
   │                       │←─Cache miss──────────│                │
   │                       │──fetch_ticker()─────→│                │
   │                       │                      │──API call────→ │
   │                       │←─BTC: $110,374.59────│                │
   │                       │──Save to cache──────→│                │
   │←─{price, source}──────│                      │                │
   │                       │                      │                │
   │──Update UI states────│                      │                │
   │  • priceSource='real'│                      │                │
   │  • priceFlash=true   │                      │                │
   │  • chartData.push()  │                      │                │
   │                       │                      │                │
   │──Render with new data│                      │                │
   │                       │                      │                │
   
[2 seconds later, repeat...]
```

---

## 🛠️ Handling Different Types of Updates

### 1. Price Updates (Real-time)

**Current Implementation**:
- **Frequency**: Every 2 seconds
- **Method**: HTTP polling to `/price-auto/`
- **Trigger**: setInterval in useEffect
- **Updates**: Price display, chart data, animations

**Code Location**: `advanced-orders/page.tsx` line 136-149

### 2. Settings Updates (Admin Changes)

**When Admin Changes Settings**:
```
Admin Board → Save Settings → API PATCH → Database Update
                                            ↓
                              Next price request uses new settings
```

**Takes Effect**: Immediately on next price fetch (within 2 seconds)

### 3. Chart Data Updates

**Every Price Update**:
```typescript
setChartData(prev => {
  const newCandle = {
    timestamp: data.timestamp,
    close: data.price,
    // ... calculate open, high, low
  };
  
  return [...prev.slice(-29), newCandle];  // Keep last 30 candles
});
```

**Result**: Rolling window of 30 data points, oldest drops off

### 4. Trade Outcome Updates

**When Trade Closes**:
```
Celery Task (runs every minute) →
Check UserTradeOutcome.target_close_time →
If time reached → Execute sell order →
Update user balance →
Mark outcome as executed
```

**File**: `fluxor_api/trades/tasks.py`

---

## 🚀 Optimizing Update Performance

### Current: HTTP Polling Every 2 Seconds

**Pros**:
- ✅ Simple to implement
- ✅ Works with any backend
- ✅ Easy to debug

**Cons**:
- ❌ Not true real-time
- ❌ Extra HTTP requests
- ❌ 2-second delay

### Future: WebSocket Integration

**Upgrade Path**:
```python
# Backend: Stream real prices via WebSocket
async def stream_real_prices(websocket):
    while True:
        price = get_price_service().get_current_price('BTC')
        await websocket.send_json({
            'price': price,
            'source': 'real',
            'timestamp': now()
        })
        await asyncio.sleep(1)  # Update every second
```

```typescript
// Frontend: Receive via WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/prices/BTC/');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updatePrice(data);  // Instant update!
};
```

---

## 🔧 Customizing Update Behavior

### Change Update Frequency

**File**: `advanced-orders/page.tsx`
```typescript
// Current: Every 2 seconds
const interval = setInterval(() => {
  updateLivePrice();
}, 2000);  // ← Change this value

// Options:
}, 1000);  // Every 1 second (faster)
}, 3000);  // Every 3 seconds (slower)
}, 5000);  // Every 5 seconds (less API calls)
```

### Change Cache Duration

**File**: `real_price_service.py`
```python
# Current: 60 second cache
cache.set(cache_key, price, 60)  # ← Change this value

# Options:
cache.set(cache_key, price, 30)   # 30 seconds (fresher data)
cache.set(cache_key, price, 120)  # 2 minutes (fewer API calls)
cache.set(cache_key, price, 300)  # 5 minutes (minimal API usage)
```

### Disable Animations

**File**: `advanced-orders/page.tsx`
```typescript
// Comment out animation triggers
// setPriceFlash(true);
// setNewDataAnimation(true);

// Or reduce duration
setTimeout(() => setPriceFlash(false), 200);  // 200ms instead of 500ms
```

---

## 📈 Monitoring Updates

### Check Update Logs

**Browser Console**:
```javascript
// Open DevTools Console (F12)
// Watch for logs:
🔄 Fetching live price from backend...
📊 Backend price data: {price: 110374.59, source: 'real'}
🌐 Price source: REAL
📈 New price from backend: 110374.59
```

**Backend Logs**:
```bash
docker logs -f trading-api-1

# Look for:
# - CCXT fetch attempts
# - CoinGecko fallbacks
# - Cache hits/misses
# - Price update requests
```

### Check Update Frequency

**Browser Console**:
```javascript
// Count updates per minute
let updateCount = 0;
const originalLog = console.log;
console.log = (...args) => {
  if (args[0]?.includes('Fetching live price')) {
    updateCount++;
  }
  originalLog(...args);
};

// After 60 seconds, check updateCount
setTimeout(() => {
  console.log('Updates per minute:', updateCount);
  // Expected: ~30 (every 2 seconds)
}, 60000);
```

---

## 🎛️ Admin Control Over Updates

### What Admins Can Control:

1. **Price Source** (Real vs Simulated)
   - Toggle: `use_real_prices`
   - Effect: Changes where prices come from

2. **Trade Outcomes** (Win/Loss Probabilities)
   - Settings: `active_win_rate_percentage`, etc.
   - Effect: Changes trade results, affects simulated price paths

3. **Update Interval** (Backend WebSocket - if using)
   - Setting: `update_interval_seconds`
   - Effect: Changes how often WebSocket sends data

4. **Price Volatility** (Simulated Mode Only)
   - Setting: `price_volatility_percentage`
   - Effect: Changes how much simulated prices fluctuate

### What Users See:

**Real Prices ON**:
- Badge shows: "Real Prices" (blue globe icon)
- Prices match actual market (BTC: $110,374.59)
- Chart shows real market movements
- Updates reflect actual trading activity

**Real Prices OFF**:
- Badge shows: "Simulated" (yellow chart icon)  
- Prices follow predetermined paths
- Chart shows calculated movements
- Updates follow trade outcome logic

---

## 🔄 Complete Update Lifecycle Example

### User Places Trade → Watch Price Updates

**Step 1: User Places Buy Order**
```
User clicks "Place Order" →
POST /api/trading/execute/ →
BiasedTradeExecutor.determine_trade_outcome() →
Result: WIN, 10% profit, 300 seconds →
UserTradeOutcome created →
Price simulator initialized
```

**Step 2: Price Updates Begin**
```
Every 2 seconds:
  Frontend polls /price-auto/ →
  Backend checks: use_real_prices? →
  
  If TRUE:
    Get from Binance: $110,374.59 →
    Return: {price: 110374.59, source: 'real'}
  
  If FALSE:
    Get from Simulator based on trade outcome →
    Return: {price: 43892.15, source: 'simulated'}
```

**Step 3: UI Updates**
```
Receive price →
Flash animation →
Add to chart →
Show new data highlight →
Display source badge
```

**Step 4: Trade Closes (After 300s)**
```
Celery task detects target_close_time reached →
Execute sell order at target price →
Calculate actual profit/loss →
Update user balance →
Mark trade as executed
```

---

## 📚 Key Files Reference

| File | Purpose | Update Handling |
|------|---------|----------------|
| `real_price_service.py` | Fetch real prices | Caches for 60s, tries CCXT→CoinGecko |
| `market_data_views.py` | API endpoints | Routes to real or simulated |
| `advanced-orders/page.tsx` | Frontend UI | Polls every 2s, renders updates |
| `biased_trade_executor.py` | Trade outcomes | Determines win/loss on trade placement |
| `price_simulator.py` | Simulated prices | Generates price paths for trades |
| `board/page.tsx` | Admin controls | Saves settings to backend |

---

## 💡 Best Practices

### For Development:
1. Use **simulated prices** (faster, no API limits)
2. Enable **console logging** to see update flow
3. Test with different update intervals
4. Monitor browser network tab

### For Production:
1. Use **real prices** for authenticity
2. Monitor API rate limits (CoinGecko: 50/min)
3. Set reasonable polling interval (2-5 seconds)
4. Use caching to reduce API calls
5. Have fallback to simulated if APIs fail

### For Testing:
1. Toggle real/simulated to compare behavior
2. Check `data.source` in responses
3. Verify cache is working (same price for 60s)
4. Test with different cryptocurrencies

---

## 🐛 Troubleshooting Updates

### Problem: Prices Not Updating

**Check**:
1. Is timer running? (Console should log "Fetching live price...")
2. Is API responding? (Check Network tab in DevTools)
3. Is auth token valid? (401 errors = re-login needed)
4. Is backend running? (`docker ps` - check trading-api-1)

### Problem: Still Showing Old Prices

**Solutions**:
1. Hard refresh: `Cmd/Ctrl + Shift + R`
2. Clear cache: DevTools → Application → Clear storage
3. Restart web container: `docker restart trading-web-1`
4. Check if new build was created (board page size should be ~6.67KB)

### Problem: Real Prices Not Working

**Check**:
1. Is toggle ON in admin board?
2. Test directly: `docker exec trading-api-1 python manage.py shell -c "..."`
3. Check internet connection from container
4. Verify API keys if using authenticated access

---

## 📊 Update Flow Summary

**Quick Reference**:

```
USER ACTION → FRONTEND TIMER → API REQUEST → BACKEND LOGIC → DATA SOURCE
                                                                    ↓
                                                         Real Exchange or Database
                                                                    ↓
                                                            RESPONSE DATA
                                                                    ↓
                                                         FRONTEND RECEIVES
                                                                    ↓
                                                           STATE UPDATES
                                                                    ↓
                                                           UI RE-RENDERS
                                                                    ↓
                                                       USER SEES NEW PRICE
```

**Timing**: Total round-trip ~100-500ms, repeats every 2 seconds

---

**Last Updated**: October 11, 2025  
**Current System**: ✅ Polling-based with smart endpoint  
**Future**: 🚀 WebSocket streaming for true real-time updates

