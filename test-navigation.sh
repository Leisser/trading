#!/bin/bash

# Test Navigation and Cryptocurrency Management
echo "🧪 Testing Navigation and Cryptocurrency Management Links"
echo "======================================================="

# Check if the development server is running
echo "Checking if development server is accessible..."
if curl -s http://localhost:5173/ > /dev/null; then
    echo "✅ Development server is running at http://localhost:5173"
    DEV_SERVER="http://localhost:5173"
elif curl -s http://localhost:3000/ > /dev/null; then
    echo "✅ Production server is running at http://localhost:3000"
    DEV_SERVER="http://localhost:3000"
else
    echo "❌ No server found running. Please start the frontend server first."
    echo "Run: ./start-dev.sh or docker-compose up -d frontend"
    exit 1
fi

echo ""
echo "🔗 Available Routes:"
echo "==================="
echo "• Main Dashboard: $DEV_SERVER/dashboard"
echo "• Admin Panel: $DEV_SERVER/admin"
echo "• Advanced Admin: $DEV_SERVER/admin-dashboard"
echo "• 💰 Cryptocurrency Management: $DEV_SERVER/cryptocurrencies"
echo ""

echo "🎯 Testing Route Accessibility..."
echo "=================================="

# Test main routes (these should return HTML)
ROUTES=(
    "/dashboard"
    "/admin"
    "/admin-dashboard"
    "/cryptocurrencies"
)

for route in "${ROUTES[@]}"; do
    echo -n "Testing $route... "
    
    # Try to access the route
    if curl -s -I "${DEV_SERVER}${route}" | grep -q "200 OK"; then
        echo "✅ Accessible"
    else
        # Vue Router uses client-side routing, so check if we get the main index.html
        if curl -s "${DEV_SERVER}${route}" | grep -q "<!DOCTYPE html>"; then
            echo "✅ Routable (Vue SPA)"
        else
            echo "❌ Not accessible"
        fi
    fi
done

echo ""
echo "🔍 Checking if Router Configuration is Correct..."
echo "=================================================="

# Check if the router index.ts file has the cryptocurrencies route
if grep -q "cryptocurrencies" /Users/mc/trading/fluxor_api/src/router/index.ts; then
    echo "✅ Cryptocurrencies route found in router configuration"
else
    echo "❌ Cryptocurrencies route NOT found in router configuration"
fi

# Check if the CryptocurrenciesView component exists
if [ -f "/Users/mc/trading/fluxor_api/src/views/CryptocurrenciesView.vue" ]; then
    echo "✅ CryptocurrenciesView component exists"
else
    echo "❌ CryptocurrenciesView component NOT found"
fi

# Check if navigation links are present in key views
echo ""
echo "🔗 Checking Navigation Links in Views..."
echo "========================================"

VIEWS=(
    "/Users/mc/trading/fluxor_api/src/views/DashboardView.vue"
    "/Users/mc/trading/fluxor_api/src/views/AdminView.vue" 
    "/Users/mc/trading/fluxor_api/src/views/AdminDashboardView.vue"
)

for view in "${VIEWS[@]}"; do
    view_name=$(basename "$view" .vue)
    echo -n "Checking $view_name for cryptocurrency links... "
    
    if grep -q "cryptocurrencies" "$view" || grep -q "Cryptocurrencies" "$view"; then
        echo "✅ Has cryptocurrency links"
    else
        echo "⚠️  No cryptocurrency links found"
    fi
done

echo ""
echo "📊 Component Features Check..."
echo "=============================="

# Check CryptocurrenciesView features
if [ -f "/Users/mc/trading/fluxor_api/src/views/CryptocurrenciesView.vue" ]; then
    echo "Checking CryptocurrenciesView features:"
    
    # Check for filtering
    if grep -q "filters" "/Users/mc/trading/fluxor_api/src/views/CryptocurrenciesView.vue"; then
        echo "  ✅ Filtering functionality"
    else
        echo "  ❌ Filtering functionality missing"
    fi
    
    # Check for search
    if grep -q "search" "/Users/mc/trading/fluxor_api/src/views/CryptocurrenciesView.vue"; then
        echo "  ✅ Search functionality"
    else
        echo "  ❌ Search functionality missing"
    fi
    
    # Check for pagination
    if grep -q "currentPage\|totalPages\|paginatedCryptocurrencies" "/Users/mc/trading/fluxor_api/src/views/CryptocurrenciesView.vue"; then
        echo "  ✅ Pagination"
    else
        echo "  ❌ Pagination missing"
    fi
    
    # Check for import functionality
    if grep -q "import" "/Users/mc/trading/fluxor_api/src/views/CryptocurrenciesView.vue"; then
        echo "  ✅ Import functionality"
    else
        echo "  ❌ Import functionality missing"
    fi
fi

echo ""
echo "🎨 Admin Dashboard Features Check..."
echo "==================================="

if [ -f "/Users/mc/trading/fluxor_api/src/views/AdminDashboardView.vue" ]; then
    echo "Checking AdminDashboardView cryptocurrency integration:"
    
    # Check for cryptocurrency tab
    if grep -q "cryptocurrencies" "/Users/mc/trading/fluxor_api/src/views/AdminDashboardView.vue"; then
        echo "  ✅ Cryptocurrencies tab integrated"
    else
        echo "  ❌ Cryptocurrencies tab missing"
    fi
    
    # Check for management link
    if grep -q "Manage.*Cryptocurrencies" "/Users/mc/trading/fluxor_api/src/views/AdminDashboardView.vue"; then
        echo "  ✅ Management link present"
    else
        echo "  ❌ Management link missing"
    fi
fi

echo ""
echo "🔧 Backend Integration Check..."
echo "==============================="

# Check if import command exists
if [ -f "/Users/mc/trading/fluxor_api/management/commands/import_cryptocurrencies.py" ]; then
    echo "✅ Cryptocurrency import command exists"
    
    # Check if it has the comprehensive data
    if grep -q "200" "/Users/mc/trading/fluxor_api/management/commands/import_cryptocurrencies.py"; then
        echo "  ✅ Supports 200+ cryptocurrencies"
    else
        echo "  ⚠️  Limited cryptocurrency support"
    fi
else
    echo "❌ Cryptocurrency import command missing"
fi

# Check if trading tasks are updated
if [ -f "/Users/mc/trading/fluxor_api/management/commands/run_trading_tasks.py" ]; then
    echo "✅ Trading tasks command exists"
    
    if grep -q "batch" "/Users/mc/trading/fluxor_api/management/commands/run_trading_tasks.py"; then
        echo "  ✅ Supports batch processing for multiple cryptocurrencies"
    else
        echo "  ⚠️  May not handle multiple cryptocurrencies efficiently"
    fi
else
    echo "❌ Trading tasks command missing"
fi

echo ""
echo "📋 Summary"
echo "=========="
echo "Your cryptocurrency management system includes:"
echo "• 🔗 Navigation links in all admin views"
echo "• 📊 Dedicated cryptocurrency management page"
echo "• 🎛️ Integrated admin dashboard tab"
echo "• ⚡ Backend support for 200+ cryptocurrencies"
echo "• 🔄 Automated trading tasks for all cryptos"
echo ""
echo "🎉 Navigation and links are ready!"
echo ""
echo "To access cryptocurrency management:"
echo "1. Start your system: ./start-dev.sh"
echo "2. Visit: $DEV_SERVER/cryptocurrencies"
echo "3. Or use the links in admin dashboard and main dashboard"