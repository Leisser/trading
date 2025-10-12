# Troubleshooting Chart Data Display

## 🔍 **Quick Diagnosis Steps**

### **Step 1: Check if you're signed in**
The API requires authentication. If you're not signed in:
- Visit `http://localhost:5173/signin`
- Sign in with your credentials
- Then go to `http://localhost:5173/index/advanced-orders`

### **Step 2: Open Browser Console (F12)**
Look for these console logs:

✅ **Success logs:**
```
📊 Loading chart data from backend...
⏱️ Time interval: seconds
📈 Backend chart data loaded: {...}
✅ Loaded 31 chart data points from backend
```

❌ **Error logs:**
```
Failed to load chart data from backend, using fallback
⚠️ No chart data available from backend, using fallback
401 Unauthorized
```

### **Step 3: Check Network Tab**
1. Open Developer Tools (F12)
2. Go to "Network" tab
3. Filter by "Fetch/XHR"
4. Look for request to: `combined-chart/`
5. Check the response:
   - **200 OK** → Data loaded successfully
   - **401 Unauthorized** → Sign in required
   - **500 Error** → Backend issue

### **Step 4: Verify Backend is Running**
```bash
# Check API container logs
docker logs trading-api-1 --tail 20

# Should see:
# "GET /api/admin/market/combined-chart/" 200
```

### **Step 5: Test API Directly**
```bash
# Get authentication token
TOKEN=$(docker exec trading-api-1 python manage.py shell -c "
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()
user = User.objects.get(email='admin@fluxor.pro')
refresh = RefreshToken.for_user(user)
print(str(refresh.access_token))
" 2>/dev/null | tail -1)

# Test the endpoint
curl -X GET "http://localhost:8000/api/admin/market/combined-chart/?symbol=BTC&limit=5&interval=seconds" \
  -H "Authorization: Bearer $TOKEN" \
  -s | jq '.count, .interval'

# Should return:
# 6
# "seconds"
```

## 🛠️ **Common Issues & Fixes**

### **Issue 1: Not Signed In**
**Symptoms:**
- 401 Unauthorized errors
- Falls back to mock data
- Console shows "Failed to load chart data"

**Fix:**
1. Go to `/signin`
2. Sign in with your credentials
3. Return to `/index/advanced-orders`

### **Issue 2: Old Browser Cache**
**Symptoms:**
- Changes not appearing
- Old code still running

**Fix:**
```bash
# Hard refresh browser
# Chrome/Firefox: Ctrl+Shift+R (Windows/Linux)
# Chrome/Firefox: Cmd+Shift+R (Mac)

# Or clear browser cache:
# Chrome: Settings → Privacy → Clear browsing data
# Firefox: Options → Privacy → Clear Data
```

### **Issue 3: Frontend Not Updated**
**Symptoms:**
- Console logs missing
- Old behavior persists

**Fix:**
```bash
# Rebuild web container without cache
docker-compose build --no-cache web
docker-compose up -d web

# Wait 30 seconds for build to complete
# Then hard refresh browser (Ctrl+Shift+R)
```

### **Issue 4: Backend Data Missing**
**Symptoms:**
- API returns empty chart_data array
- Count is 0

**Fix:**
```bash
# Trigger Celery task to generate initial data
docker exec trading-celery_worker-1 python manage.py shell -c "
from core.tasks import generate_initial_chart_data
generate_initial_chart_data.delay()
"

# Wait 10 seconds, then refresh page
```

### **Issue 5: Token Expired**
**Symptoms:**
- Was working, then stopped
- 401 errors after some time

**Fix:**
- The frontend has automatic token refresh
- If it still fails, sign out and sign in again

## ✅ **Verification Checklist**

After fixing issues, verify everything is working:

- [ ] Can access `/index/advanced-orders` without redirects
- [ ] Browser console shows "✅ Loaded X chart data points from backend"
- [ ] Network tab shows 200 OK for `combined-chart/` request
- [ ] Chart displays candlesticks or line chart
- [ ] Can see price updates in real-time
- [ ] Switching time intervals (seconds/minutes/hours) works

## 🚀 **Expected Behavior**

When everything is working correctly:

1. **Initial Load:**
   - Fetches 31 data points from backend
   - Displays chart with candlesticks/lines
   - Shows current price

2. **Live Updates:**
   - New price data every 2 seconds (seconds interval)
   - Chart updates with new candle
   - Smooth animation

3. **Interval Switching:**
   - Clicking seconds/minutes/hours button
   - Chart reloads with new interval data
   - Console logs show new interval

## 📞 **Still Not Working?**

Check the logs:
```bash
# API logs
docker logs trading-api-1 --tail 50

# Web logs  
docker logs trading-web-1 --tail 50

# Celery logs
docker logs trading-celery_worker-1 --tail 50
```

Look for error messages and check the specific endpoint that's failing.
