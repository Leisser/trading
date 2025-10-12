# Verify Backend Data is Loading - Step by Step Guide

## 🎯 **How to Verify Data Comes from Backend**

If chart data changes when you refresh, it means you're seeing fallback/mock data instead of backend data. Here's how to verify and fix:

---

## 🔍 **Step-by-Step Verification**

### **Step 1: Sign In**
```
1. Go to: http://localhost:5173/signin
2. Email: admin@fluxor.pro
3. Password: admin123
4. Click "Sign In"
```

### **Step 2: Open Browser Console (F12)**
```
1. Press F12 (or right-click → Inspect)
2. Go to "Console" tab
3. Keep it open while navigating
```

### **Step 3: Visit Automated Strategies**
```
1. Go to: http://localhost:5173/index/automated-strategies
2. Watch console for these logs:
```

**✅ Success - Backend Data Loading:**
```javascript
✅ Loaded trading pairs from backend: {results: [...]}
📊 Loading chart for: BTC/USD
⏱️ Time interval: seconds
📊 Loading chart data from backend...
📈 Backend chart data loaded: {count: 31, chart_data: [...]}
✅ Loaded 31 chart data points from backend
```

**❌ Failure - Fallback Data:**
```javascript
⚠️ Failed to load trading pairs from backend, using fallback
⚠️ No chart data available from backend, using fallback
Error loading chart data from backend: ...
```

### **Step 4: Check Network Tab**
```
1. In Developer Tools, go to "Network" tab
2. Filter by "Fetch/XHR"
3. Look for these requests:
```

**Expected Requests:**
- `GET /api/cryptocurrencies/` → Status **200 OK**
- `GET /api/balance/` → Status **200 OK**
- `GET /api/admin/market/combined-chart/?symbol=BTC&limit=30&interval=seconds` → Status **200 OK**
- `GET /api/admin/market/price-auto/?symbol=BTC` → Status **200 OK** (every 2 seconds)
- `POST /api/admin/market/store-data-point/` → Status **200 OK** or **201 Created**

**If you see:**
- **401 Unauthorized** → Sign in again
- **404 Not Found** → Backend endpoint missing
- **500 Internal Server Error** → Check backend logs

### **Step 5: Test Data Persistence**
```
1. Note the current chart pattern
2. Refresh the page (F5)
3. Check if chart pattern is:
   - ✅ SAME → Data from backend (persistent)
   - ❌ DIFFERENT → Data from fallback (generated fresh)
```

---

## 🛠️ **Common Issues & Fixes**

### **Issue 1: No API Requests Visible**

**Symptoms:**
- No `combined-chart` requests in Network tab
- Console shows fallback messages
- Chart changes on refresh

**Diagnosis:**
```bash
# Check if API is running
docker ps | grep api

# Check API logs
docker logs trading-api-1 --tail 50
```

**Fix:**
```bash
# Restart API container
docker-compose restart api

# Verify it's healthy
docker logs trading-api-1 --tail 20
```

---

### **Issue 2: 401 Unauthorized Errors**

**Symptoms:**
- All API requests return 401
- Console shows authentication errors
- Redirects to sign-in page

**Diagnosis:**
- JWT token expired or missing
- Not signed in properly

**Fix:**
1. Sign out: `http://localhost:5173/signout`
2. Sign in again: `http://localhost:5173/signin`
3. Revisit page
4. Check console for successful requests

---

### **Issue 3: Backend Returns Empty Data**

**Symptoms:**
- API returns 200 OK
- But `chart_data` array is empty
- Falls back to mock data

**Diagnosis:**
```bash
# Check database for chart data
docker exec trading-db-1 psql -U fluxor -d fluxor -c \
  "SELECT COUNT(*), symbol FROM market_data_chartdatapoint GROUP BY symbol;"
```

**Fix:**
```bash
# Regenerate chart data
docker exec trading-celery_worker-1 python manage.py shell -c "
from core.tasks import generate_initial_chart_data
generate_initial_chart_data()
"

# Wait 5 seconds, then refresh page
```

---

### **Issue 4: CORS or Network Errors**

**Symptoms:**
- Console shows CORS errors
- Failed to fetch errors
- Network requests show (failed)

**Diagnosis:**
- Backend not accessible from frontend
- CORS configuration issue

**Fix:**
```bash
# Check if backend is accessible
curl http://localhost:8000/api/cryptocurrencies/

# If not accessible, restart nginx
docker-compose restart nginx
```

---

## 📊 **Database Verification**

### **Check Chart Data Exists**
```bash
docker exec trading-db-1 psql -U fluxor -d fluxor -c "
SELECT COUNT(*), symbol 
FROM market_data_chartdatapoint 
GROUP BY symbol;
"
```

**Expected Output:**
```
 count | symbol
-------+--------
    30 | BTC
    30 | ETH
    30 | SOL
    30 | XRP
    30 | ADA
```

### **Check Recent Data**
```bash
docker exec trading-db-1 psql -U fluxor -d fluxor -c "
SELECT symbol, timestamp, close_price, source 
FROM market_data_chartdatapoint 
ORDER BY timestamp DESC 
LIMIT 5;
"
```

**Expected Output:**
```
 symbol |         timestamp          | close_price |   source
--------+----------------------------+-------------+------------
 BTC    | 2025-10-12 10:05:30+00     | 43762.10    | simulated
 ETH    | 2025-10-12 10:05:30+00     | 2654.25     | simulated
 ...
```

---

## 🧪 **API Testing**

### **Test Chart Data Endpoint**
```bash
# Get admin token
TOKEN=$(docker exec trading-api-1 python manage.py shell -c "
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()
user = User.objects.get(email='admin@fluxor.pro')
print(str(RefreshToken.for_user(user).access_token))
" 2>/dev/null | tail -1)

# Test endpoint
curl -X GET "http://localhost:8000/api/admin/market/combined-chart/?symbol=BTC&limit=5&interval=seconds" \
  -H "Authorization: Bearer $TOKEN" \
  -s | jq '.count, .chart_data[0].timestamp'

# Should return:
# 6
# "2025-10-12T10:00:00.000000+00:00"
```

### **Test Multiple Times**
```bash
# First request
curl -X GET "http://localhost:8000/api/admin/market/combined-chart/?symbol=BTC&limit=5&interval=seconds" \
  -H "Authorization: Bearer $TOKEN" \
  -s | jq '.chart_data[0].timestamp'

# Second request (should be SAME timestamp if from backend)
curl -X GET "http://localhost:8000/api/admin/market/combined-chart/?symbol=BTC&limit=5&interval=seconds" \
  -H "Authorization: Bearer $TOKEN" \
  -s | jq '.chart_data[0].timestamp'

# If timestamps are SAME → Backend data
# If timestamps are DIFFERENT → Generating fresh data (problem!)
```

---

## ✅ **What Should Happen**

### **On Initial Page Load**
```
1. Sign in → Get JWT tokens
2. Visit page
3. Console logs:
   ✅ Loaded trading pairs from backend
   📊 Loading chart for: BTC/USD
   ⏱️ Time interval: seconds
   📊 Loading chart data from backend...
   📈 Backend chart data loaded: {...}
   ✅ Loaded 31 chart data points from backend

4. Network tab shows:
   GET /api/cryptocurrencies/ → 200 OK
   GET /api/balance/ → 200 OK
   GET /api/admin/market/combined-chart/ → 200 OK
```

### **On Page Refresh**
```
1. Press F5 to refresh
2. Same console logs as above
3. Chart displays SAME data (not random new data)
4. Network tab shows same API requests
5. Data is PERSISTENT because it's from PostgreSQL
```

### **On Time Interval Change**
```
1. Click "Minutes" button
2. Console logs:
   📊 Loading chart for: BTC/USD
   ⏱️ Time interval: minutes
   📊 Loading chart data from backend...
   ✅ Loaded 31 chart data points from backend

3. Chart reloads with minute-spaced data
4. Updates every 60 seconds (not 2 seconds)
```

---

## 🎯 **Quick Diagnostic Commands**

```bash
# 1. Check web container logs
docker logs trading-web-1 --tail 20

# 2. Check API logs for chart requests
docker logs trading-api-1 --tail 100 | grep combined-chart

# 3. Check database has data
docker exec trading-db-1 psql -U fluxor -d fluxor -c \
  "SELECT COUNT(*) FROM market_data_chartdatapoint;"

# 4. Check if API is accessible
curl http://localhost:8000/api/cryptocurrencies/ -s | jq '.results | length'

# 5. Verify web container is running
docker ps | grep web
```

---

## 💡 **Key Indicators**

### **✅ Data IS from Backend:**
- Console shows: "✅ Loaded X chart data points from backend"
- Network tab shows: 200 OK for combined-chart
- Chart stays SAME on page refresh
- Timestamps in data don't change randomly
- Database query shows matching data

### **❌ Data is NOT from Backend (Fallback):**
- Console shows: "⚠️ No chart data available from backend, using fallback"
- Network tab shows: 401 or no combined-chart request
- Chart CHANGES on page refresh
- Data is randomly generated each time
- No database matching data

---

## 🚀 **Final Check**

After signing in and visiting a page, run this test:

```bash
# Monitor API requests in real-time
docker logs -f trading-api-1 | grep -E "(combined-chart|cryptocurrencies|price-auto)"
```

Then:
1. Refresh the page
2. Watch the logs
3. You should see:
   ```
   GET /api/cryptocurrencies/
   GET /api/admin/market/combined-chart/?symbol=BTC&limit=30&interval=seconds
   GET /api/admin/market/price-auto/?symbol=BTC
   POST /api/admin/market/store-data-point/
   ```

If you see these logs, the backend integration is working! 🎉

If you don't see these logs, the frontend is using fallback data and we need to debug why the API calls aren't being made.
