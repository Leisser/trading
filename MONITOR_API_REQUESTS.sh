#!/bin/bash

echo "🔍 Monitoring API Requests in Real-Time"
echo "======================================"
echo ""
echo "📋 Instructions:"
echo "1. Keep this terminal window open"
echo "2. In your browser, visit:"
echo "   - http://localhost:5173/index/automated-strategies"
echo "   - http://localhost:5173/index/leverage-trading"
echo "3. Watch for API requests below"
echo ""
echo "✅ If you see 'combined-chart' requests → Backend data is loading"
echo "❌ If you don't see them → Frontend is using fallback data"
echo ""
echo "======================================"
echo "Watching API logs..."
echo ""

docker logs -f trading-api-1 2>&1 | grep --line-buffered -E "(combined-chart|cryptocurrencies|price-auto|store-data-point|balance)" | while read line; do
  echo "[$(date '+%H:%M:%S')] $line"
done
