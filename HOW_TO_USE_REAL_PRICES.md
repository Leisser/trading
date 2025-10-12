# How to Use Real Cryptocurrency Prices

## ✅ FEATURE IS LIVE AND WORKING!

Real prices are now integrated and tested:
- **BTC**: $110,374.59 (live from exchanges)
- **ETH**: $3,692.08 (live from exchanges)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Enable Real Prices in Admin Board

1. Open your browser: `http://localhost/board` or `http://localhost:5173/board`

2. **Hard Refresh** the page:
   - **Mac**: `Cmd + Shift + R`
   - **Windows/Linux**: `Ctrl + Shift + R`

3. Click the **"Trading Control Settings"** button

4. Scroll to the bottom - you'll see:
   ```
   🌐 Real Price Integration
   ┌──────────────────────────────────────┐
   │ Enable fetching real cryptocurrency  │
   │ prices from exchanges                │
   │ (CoinGecko/CCXT)                     │
   │                          [Toggle ON] │
   └──────────────────────────────────────┘
   ```

5. Toggle the switch to **ENABLED** (it will turn green)

6. Click **"Save Settings"**

### Step 2: Verify Real Prices Are Active

Open Chrome DevTools/Browser Console and run:

```javascript
// Test the real price endpoint
fetch('http://localhost:8000/api/admin/market/real-price/?symbol=BTC', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
  }
})
.then(r => r.json())
.then(data => console.log('Real BTC Price:', data));
```

You should see real-time Bitcoin price!

### Step 3: Update Advanced Orders Page (Optional)

The advanced-orders page can now use real prices. Update the price fetching logic:

**Current endpoint:**
```
/api/admin/market/current-price/
```

**New smart endpoint (auto switches based on settings):**
```
/api/admin/market/price-auto/
```

---

## 📊 Available Endpoints

### 1. Auto Price (Recommended)
```
GET /api/admin/market/price-auto/?symbol=BTC
```
**Automatically uses real or simulated based on admin settings**

### 2. Real Price (Always Real)
```
GET /api/admin/market/real-price/?symbol=BTC
```
**Always fetches from exchanges (requires toggle ON)**

### 3. Real Chart Data
```
GET /api/admin/market/real-chart/?symbol=BTC&interval=hourly&days=1
```
**Get real historical candlestick data**

---

## 🎨 Frontend Integration Example

### Update Advanced Orders Page

```typescript
// Replace this:
const response = await fetch(
  `http://localhost:8000/api/admin/market/current-price/?symbol=${selectedPair.base_currency}`
);

// With this (auto-switches between real/simulated):
const response = await fetch(
  `http://localhost:8000/api/admin/market/price-auto/?symbol=${selectedPair.base_currency}`
);

const data = await response.json();
console.log('Price source:', data.source); // 'real' or 'simulated'
console.log('Price:', data.price);
```

---

## 💡 What Changes When Real Prices Are ON?

### Before (Simulated):
- Prices are generated algorithmically
- Based on predetermined win/loss outcomes
- Price movements follow a calculated path
- **Source**: Database

### After (Real):
- Prices fetched from Binance/CoinGecko every 60 seconds
- Reflects actual market conditions
- Real volatility and price movements
- **Source**: Live exchanges

### Hybrid Mode:
- Trade outcomes still controlled by admin (win/loss rates)
- But prices are REAL market prices
- Best of both worlds: control + realism

---

## 🔧 Testing Commands

### Test in Docker Container:
```bash
docker exec trading-api-1 python manage.py shell -c "
from admin_control.real_price_service import get_price_service
service = get_price_service()

# Get Bitcoin price
btc = service.get_current_price('BTC')
print(f'BTC: \${btc:,.2f}')

# Get Ethereum price
eth = service.get_current_price('ETH')
print(f'ETH: \${eth:,.2f}')

# Get multiple at once
prices = service.get_multiple_prices(['BTC', 'ETH', 'SOL'])
for symbol, price in prices.items():
    print(f'{symbol}: \${price:,.2f}')
"
```

### Test via API:
```bash
# Get your auth token first
TOKEN="your_token_here"

# Test real price endpoint
curl "http://localhost:8000/api/admin/market/real-price/?symbol=BTC" \
  -H "Authorization: Bearer $TOKEN"

# Should return:
{
  "symbol": "BTC",
  "price": 110374.59,
  "timestamp": "2025-10-11T...",
  "source": "real",
  "price_change_24h": 2.35,
  "volume_24h": 28500000000
}
```

---

## 🎯 Supported Cryptocurrencies

Currently supported (can add more):

✅ Bitcoin (BTC)  
✅ Ethereum (ETH)  
✅ Tether (USDT)  
✅ Binance Coin (BNB)  
✅ Solana (SOL)  
✅ Ripple (XRP)  
✅ Cardano (ADA)  
✅ Dogecoin (DOGE)  
✅ Tron (TRX)  
✅ Polkadot (DOT)  
✅ Polygon (MATIC)  
✅ Litecoin (LTC)  
✅ Avalanche (AVAX)  
✅ Chainlink (LINK)  
✅ Uniswap (UNI)  

---

## ⚙️ Configuration

### Where to Toggle:

**Option 1: Board Page (Easiest)**
- Go to `/board`
- Click "Trading Control Settings"
- Find "Real Price Integration" section
- Toggle ON/OFF
- Save

**Option 2: Django Admin**
- Go to `http://localhost:8000/admin/`
- Navigate to: Admin Control → Trading Settings
- Check: ☑ Use real prices
- Save

**Option 3: API**
```bash
curl -X PATCH http://localhost:8000/api/admin/settings/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"use_real_prices": true}'
```

---

## 📈 Current Test Results

```
Testing Real Prices...
BTC: $110,374.59  ✅
ETH: $3,692.08    ✅
```

**Data Sources:**
1. ✅ CCXT (Binance) - Primary
2. ✅ CoinGecko - Fallback
3. ✅ Database - Last resort

---

## 🎬 Next Steps

1. **Enable the toggle** in board settings
2. **Hard refresh** your browser (`Cmd/Ctrl + Shift + R`)
3. **Visit advanced-orders** page to see real prices in action
4. **Watch prices update** every 2 seconds with live market data

---

## 📚 Full Documentation

- **Complete Guide**: `REAL_PRICES_INTEGRATION.md`
- **Board Updates**: `BOARD_PAGE_UPDATE_SUMMARY.md`
- **Profit Settings**: `ACTIVE_MODE_PROFIT_PROBABILITY.md`

---

**Status**: ✅ READY TO USE  
**Last Tested**: October 11, 2025 - BTC: $110,374.59, ETH: $3,692.08  
**Service**: ONLINE and fetching live data from exchanges

