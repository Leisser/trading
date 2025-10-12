# Real Cryptocurrency Prices Integration

## Overview

The platform now supports **real-time cryptocurrency prices** from external exchanges and APIs. You can toggle between simulated prices (for demo/testing) and real market prices (for production trading).

## Features

✅ **Real-Time Prices** - Fetch live cryptocurrency prices from CoinGecko and CCXT exchanges  
✅ **Historical Charts** - Get real OHLCV candlestick data from Binance and other exchanges  
✅ **Multiple Data Sources** - Falls back from CCXT → CoinGecko → Simulated  
✅ **Caching** - Smart caching (60s TTL) to avoid API rate limits  
✅ **Admin Toggle** - Easy on/off switch in Django admin  
✅ **Automatic Fallback** - If real prices fail, system uses simulated prices  

## Supported Cryptocurrencies

- Bitcoin (BTC)
- Ethereum (ETH)
- Tether (USDT)
- Binance Coin (BNB)
- Solana (SOL)
- Ripple (XRP)
- Cardano (ADA)
- Dogecoin (DOGE)
- Tron (TRX)
- Polkadot (DOT)
- Polygon (MATIC)
- Litecoin (LTC)
- Avalanche (AVAX)
- Chainlink (LINK)
- Uniswap (UNI)

*More can be easily added by updating the `COINGECKO_IDS` mapping*

## How to Enable Real Prices

### Method 1: Django Admin (Recommended)

1. Go to: `http://localhost:8000/admin/`
2. Navigate to: **Admin Control** → **Trading Settings**
3. Find section: **🌐 Real Price Integration**
4. Check the box: ☑ **Use real prices**
5. Click **Save**

### Method 2: API Endpoint

```bash
curl -X PATCH http://localhost:8000/api/admin/settings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "use_real_prices": true
  }'
```

## API Endpoints

### 1. Get Real Price

**Endpoint:** `GET /api/admin/market/real-price/`

Fetches current real-time price for a cryptocurrency.

**Parameters:**
- `symbol` (optional): Cryptocurrency symbol (default: BTC)

**Example:**
```bash
curl "http://localhost:8000/api/admin/market/real-price/?symbol=BTC" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "symbol": "BTC",
  "price": 67245.50,
  "timestamp": "2025-10-11T18:30:45Z",
  "source": "real",
  "price_change_24h": 2.35,
  "high_24h": 68100.00,
  "low_24h": 66500.00,
  "volume_24h": 28500000000
}
```

### 2. Get Real Chart Data

**Endpoint:** `GET /api/admin/market/real-chart/`

Fetches historical OHLCV candlestick data.

**Parameters:**
- `symbol` (optional): Cryptocurrency symbol (default: BTC)
- `interval` (optional): 'minutely' | 'hourly' | 'daily' (default: hourly)
- `days` (optional): Number of days of history (default: 1)

**Example:**
```bash
curl "http://localhost:8000/api/admin/market/real-chart/?symbol=ETH&interval=hourly&days=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "symbol": "ETH",
  "current_price": 3245.75,
  "interval": "hourly",
  "days": 1,
  "source": "real",
  "count": 24,
  "chart_data": [
    {
      "timestamp": 1728669600,
      "open": 3200.50,
      "high": 3250.00,
      "low": 3190.00,
      "close": 3245.75,
      "volume": 1250000
    },
    ...
  ]
}
```

### 3. Get Price Auto (Smart Endpoint)

**Endpoint:** `GET /api/admin/market/price-auto/`

Automatically returns real prices if enabled, otherwise simulated prices.

**Parameters:**
- `symbol` (optional): Cryptocurrency symbol (default: BTC)

**Example:**
```bash
curl "http://localhost:8000/api/admin/market/price-auto/?symbol=BTC" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "symbol": "BTC",
  "price": 67245.50,
  "timestamp": "2025-10-11T18:30:45Z",
  "source": "real"  // or "simulated"
}
```

## Technical Architecture

### Data Sources (Priority Order)

1. **CCXT (Binance)**
   - Fastest response
   - Most accurate real-time data
   - OHLCV candlesticks available
   - No API key required for public data

2. **CoinGecko API**
   - Fallback if CCXT fails
   - Good for current prices
   - Limited historical data
   - Free tier: 50 calls/minute

3. **Simulated Prices**
   - Final fallback
   - Uses database values
   - Always available

### Caching Strategy

- **Cache Duration**: 60 seconds
- **Cache Key**: `real_price_{symbol}`
- **Benefits**:
  - Reduces API calls
  - Faster response times
  - Avoids rate limits

### Service Architecture

```
┌─────────────────────────────────────┐
│  RealPriceService (Singleton)       │
├─────────────────────────────────────┤
│  - get_current_price(symbol)        │
│  - get_historical_data(...)         │
│  - get_multiple_prices([symbols])   │
│  - get_24h_stats(symbol)            │
│  - is_available()                   │
└─────────────────────────────────────┘
          ↓
    ┌─────────────┬────────────────┐
    ↓             ↓                ↓
┌────────┐  ┌──────────┐  ┌──────────────┐
│  CCXT  │  │CoinGecko │  │  Database    │
│(Binance)│  │   API   │  │ (Fallback)   │
└────────┘  └──────────┘  └──────────────┘
```

## Frontend Integration

### Update Advanced Orders Page

Replace the current price update logic:

```typescript
// Before (Simulated)
const response = await fetch(
  `http://localhost:8000/api/admin/market/current-price/?symbol=${symbol}`
);

// After (Real or Simulated - Auto)
const response = await fetch(
  `http://localhost:8000/api/admin/market/price-auto/?symbol=${symbol}`
);
```

### Real Chart Data

```typescript
// Fetch real historical data
const response = await fetch(
  `http://localhost:8000/api/admin/market/real-chart/?symbol=${symbol}&interval=minutely&days=1`,
  { headers: { 'Authorization': `Bearer ${token}` }}
);

const data = await response.json();
const chartData = data.chart_data.map(candle => ({
  timestamp: new Date(candle.timestamp * 1000).toISOString(),
  open: candle.open,
  high: candle.high,
  low: candle.low,
  close: candle.close,
  volume: candle.volume
}));
```

## Testing

### 1. Test Real Price Service

```python
# Django shell
python manage.py shell

from admin_control.real_price_service import get_price_service

service = get_price_service()

# Check if service is available
print(service.is_available())  # Should return True

# Get Bitcoin price
btc_price = service.get_current_price('BTC')
print(f"BTC Price: ${btc_price:,.2f}")

# Get Ethereum price
eth_price = service.get_current_price('ETH')
print(f"ETH Price: ${eth_price:,.2f}")

# Get multiple prices at once
prices = service.get_multiple_prices(['BTC', 'ETH', 'SOL'])
print(prices)

# Get 24h statistics
stats = service.get_24h_stats('BTC')
print(stats)

# Get historical data
candles = service.get_historical_data('BTC', days=1, interval='hourly')
print(f"Got {len(candles)} candles")
```

### 2. Test API Endpoints

```bash
# Enable real prices first
curl -X PATCH http://localhost:8000/api/admin/settings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"use_real_prices": true}'

# Test real price endpoint
curl "http://localhost:8000/api/admin/market/real-price/?symbol=BTC" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test real chart data
curl "http://localhost:8000/api/admin/market/real-chart/?symbol=ETH&interval=hourly&days=1" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test auto endpoint (should return real prices now)
curl "http://localhost:8000/api/admin/market/price-auto/?symbol=BTC" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Test Fallback Behavior

```bash
# Disable real prices
curl -X PATCH http://localhost:8000/api/admin/settings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"use_real_prices": false}'

# Test auto endpoint (should return simulated prices now)
curl "http://localhost:8000/api/admin/market/price-auto/?symbol=BTC" \
  -H "Authorization: Bearer YOUR_TOKEN"
# Should return: "source": "simulated"
```

## Rate Limits & Best Practices

### CoinGecko Free Tier
- **50 calls/minute**
- **10,000 calls/month**
- Solution: Built-in 60s caching

### CCXT (Binance)
- **1,200 requests/minute** (public API)
- No authentication needed for public data
- Solution: Use CCXT as primary source

### Recommendations

1. **Use Auto Endpoint**: Always use `/market/price-auto/` for flexibility
2. **Cache on Frontend**: Don't poll more than once every 2-3 seconds
3. **Batch Requests**: Use `get_multiple_prices()` for multiple symbols
4. **Monitor Errors**: Log when real prices fail and fallback occurs
5. **Test Before Production**: Verify APIs are accessible from your server

## Error Handling

### Common Errors

**1. "Real prices are not enabled"**
```json
{
  "error": "Real prices are not enabled. Please enable in Trading Settings."
}
```
**Solution**: Enable `use_real_prices` in admin settings

**2. "Real price service is currently unavailable"**
```json
{
  "error": "Real price service is currently unavailable"
}
```
**Solution**: Check internet connection, API status, or use simulated prices

**3. "Unable to fetch price for {symbol}"**
```json
{
  "error": "Unable to fetch price for XYZ"
}
```
**Solution**: Symbol not supported or API is down, check symbol spelling

### Automatic Fallback

The system automatically falls back through:
1. CCXT → 2. CoinGecko → 3. Database → 4. Error

This ensures the platform always has price data available.

## Production Deployment

### Environment Variables (Optional)

For authenticated API access (higher rate limits):

```bash
# .env
COINGECKO_API_KEY=your_api_key_here
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

### Docker Considerations

Ensure the API container has internet access:

```yaml
# docker-compose.yml
api:
  ...
  dns:
    - 8.8.8.8
    - 8.8.4.4
```

### Monitoring

Add logging to track:
- API success/failure rates
- Fallback occurrences
- Response times
- Cache hit rates

## Future Enhancements

Potential improvements:
- [ ] WebSocket real-time price streams
- [ ] Support for more exchanges (Coinbase, Kraken, etc.)
- [ ] Custom API key configuration through admin
- [ ] Price alerts based on real market data
- [ ] Historical price database storage
- [ ] Price aggregation from multiple sources

## Troubleshooting

### Q: Real prices not working?
**A**: Check:
1. Is `use_real_prices` enabled in admin?
2. Does the server have internet access?
3. Are API services (CoinGecko/Binance) operational?
4. Check Django logs for specific errors

### Q: Prices seem outdated?
**A**: Prices are cached for 60 seconds. Wait 60s or clear cache:
```python
from django.core.cache import cache
cache.clear()
```

### Q: Can I add more cryptocurrencies?
**A**: Yes! Edit `fluxor_api/admin_control/real_price_service.py` and add to `COINGECKO_IDS` dictionary.

### Q: How to test without enabling for all users?
**A**: Use the `/market/real-price/` endpoint directly (it always returns real prices if available, regardless of the toggle).

---

**Status**: ✅ Fully Implemented and Ready to Use  
**Version**: 1.0.0  
**Last Updated**: October 11, 2025  
**Dependencies**: `ccxt==4.1.77`, `pycoingecko==3.1.0`

