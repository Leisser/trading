#!/bin/bash

# Fluxor Deployment Validation Script
# This script validates that all services are running correctly

set -e

echo "🔍 Validating Fluxor deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a service is responding
check_service() {
    local name=$1
    local url=$2
    local expected_status=${3:-200}
    
    echo -n "Checking $name... "
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "$expected_status"; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        return 1
    fi
}

# Function to check Docker service
check_docker_service() {
    local service_name=$1
    local container_name=$2
    
    echo -n "Checking Docker service $service_name... "
    
    if docker-compose ps "$service_name" | grep -q "Up"; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        return 1
    fi
}

echo "📊 Checking Docker services..."
check_docker_service "web" "trading-web-1"
check_docker_service "trading_tasks" "trading-trading_tasks-1"
check_docker_service "db" "trading-db-1"
check_docker_service "redis" "trading-redis-1"
check_docker_service "dashboard" "trading-dashboard-1"

echo ""
echo "🌐 Checking HTTP endpoints..."

# Check Next.js web application
check_service "Next.js Web App" "http://localhost:5173"

# Check Django API (if running)
check_service "Django API" "http://localhost:8000/api/" 200

# Check Dashboard
check_service "Dashboard" "http://localhost:3001"

# Check pgAdmin
check_service "pgAdmin" "http://localhost:5050"

echo ""
echo "🗄️  Checking database connectivity..."

# Check if we can connect to the database
if docker-compose exec -T db psql -U fluxor -d fluxor -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "Database connection: ${GREEN}✅ OK${NC}"
else
    echo -e "Database connection: ${RED}❌ FAILED${NC}"
fi

# Check if cryptocurrency data exists
crypto_count=$(docker-compose exec -T trading_tasks python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluxor_api.settings')
django.setup()
from trades.models import Cryptocurrency
print(Cryptocurrency.objects.count())
" 2>/dev/null || echo "0")

if [ "$crypto_count" -gt 50 ]; then
    echo -e "Cryptocurrency data: ${GREEN}✅ OK ($crypto_count records)${NC}"
else
    echo -e "Cryptocurrency data: ${YELLOW}⚠️  Only $crypto_count records found${NC}"
fi

echo ""
echo "📋 Deployment Summary:"
echo "======================"
echo "🌐 Next.js Web App: http://localhost:5173"
echo "🔧 Django API: http://localhost:8000/api/"
echo "📊 Dashboard: http://localhost:3001"
echo "🗄️  Database Admin: http://localhost:5050"
echo ""
echo "✅ Validation complete!"
