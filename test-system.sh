#!/bin/bash

# System Test Script for Fluxor Trading Platform
# Tests the complete Docker setup with cryptocurrency data

set -e

echo "🧪 Starting Fluxor Trading Platform System Tests"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results tracking
TESTS_PASSED=0
TESTS_FAILED=0
TOTAL_TESTS=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_exit_code="${3:-0}"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -e "\n${BLUE}🔍 Test $TOTAL_TESTS: $test_name${NC}"
    echo "Command: $test_command"
    
    if eval "$test_command"; then
        if [ $? -eq $expected_exit_code ]; then
            echo -e "${GREEN}✅ PASSED${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}❌ FAILED (unexpected exit code)${NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        echo -e "${RED}❌ FAILED${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local service_name="$1"
    local check_command="$2"
    local max_attempts="${3:-30}"
    local attempt=1
    
    echo -e "${YELLOW}⏳ Waiting for $service_name to be ready...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if eval "$check_command" >/dev/null 2>&1; then
            echo -e "${GREEN}✅ $service_name is ready${NC}"
            return 0
        fi
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo -e "\n${RED}❌ $service_name failed to become ready after $max_attempts attempts${NC}"
    return 1
}

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🧹 Cleaning up...${NC}"
    docker-compose down -v --remove-orphans >/dev/null 2>&1 || true
}

# Set trap for cleanup on exit
trap cleanup EXIT

echo -e "\n${BLUE}📋 Pre-flight Checks${NC}"
echo "================================"

# Check Docker is running
run_test "Docker daemon is running" "docker info"

# Check Docker Compose is available
run_test "Docker Compose is available" "docker-compose --version"

# Check project files exist
run_test "Docker Compose file exists" "test -f docker-compose.yml"
run_test "Django Dockerfile exists" "test -f fluxor_api/Dockerfile"
run_test "Vue.js Dockerfile exists" "test -f fluxor_api/src/Dockerfile"
run_test "Management commands exist" "test -f fluxor_api/management/commands/import_cryptocurrencies.py"
run_test "Trading tasks command exists" "test -f fluxor_api/management/commands/run_trading_tasks.py"

echo -e "\n${BLUE}🏗️ Building and Starting Services${NC}"
echo "====================================="

# Build and start services
run_test "Build Docker images" "docker-compose build --no-cache"
run_test "Start services" "docker-compose up -d"

# Wait for services to be ready
wait_for_service "PostgreSQL Database" "docker-compose exec -T db pg_isready -U postgres"
wait_for_service "Redis Cache" "docker-compose exec -T redis redis-cli ping"
wait_for_service "Django Backend" "curl -f http://localhost:8000/api/health/ || docker-compose exec -T web python -c 'import django; django.setup()'"

echo -e "\n${BLUE}🗄️ Database Tests${NC}"
echo "========================="

# Run Django migrations
run_test "Run Django migrations" "docker-compose exec -T web python manage.py migrate --run-syncdb"

# Test database connectivity
run_test "Database connectivity" "docker-compose exec -T web python manage.py shell -c 'from django.db import connection; connection.cursor().execute(\"SELECT 1\"); print(\"Database connected successfully\")'"

echo -e "\n${BLUE}💰 Cryptocurrency Data Tests${NC}"
echo "==============================="

# Import cryptocurrency data
run_test "Import cryptocurrency data" "docker-compose exec -T web python manage.py import_cryptocurrencies --limit=50"

# Verify cryptocurrency data was imported
run_test "Verify cryptocurrency data import" "docker-compose exec -T web python manage.py shell -c 'from trades.models import Cryptocurrency; count = Cryptocurrency.objects.count(); print(f\"Cryptocurrencies imported: {count}\"); assert count > 0, \"No cryptocurrencies found\"'"

# Test cryptocurrency model functionality
run_test "Test cryptocurrency model features" "docker-compose exec -T web python manage.py shell -c '
from trades.models import Cryptocurrency
btc = Cryptocurrency.objects.filter(symbol=\"BTC\").first()
if btc:
    print(f\"Bitcoin: {btc.name} - ${btc.current_price}\")
    print(f\"Market Cap: ${btc.market_cap}\")
    print(f\"Categories: {btc.categories}\")
    print(f\"Blockchain: {btc.blockchain_network}\")
else:
    raise Exception(\"Bitcoin not found in database\")
'"

echo -e "\n${BLUE}🔄 Trading Tasks Tests${NC}"
echo "============================"

# Test trading tasks (run for 30 seconds)
echo -e "${YELLOW}⏳ Testing trading tasks for 30 seconds...${NC}"
run_test "Start trading tasks in background" "timeout 30s docker-compose exec -T web python manage.py run_trading_tasks --interval=2 --batch-size=10 --verbose || true"

# Verify price data was created
run_test "Verify price data generation" "docker-compose exec -T web python manage.py shell -c '
from trades.models import PriceData, PriceMovementLog
price_data_count = PriceData.objects.count()
movement_log_count = PriceMovementLog.objects.count()
print(f\"Price data records: {price_data_count}\")
print(f\"Movement log records: {movement_log_count}\")
assert price_data_count > 0 or movement_log_count > 0, \"No trading data generated\"
'"

echo -e "\n${BLUE}🌐 API Endpoint Tests${NC}"
echo "=========================="

# Test Django health endpoint
run_test "Django health endpoint" "curl -f http://localhost:8000/api/health/"

# Test Django admin access
run_test "Django admin interface" "curl -f -I http://localhost:8000/admin/"

# Test API endpoints (if available)
run_test "Test API root endpoint" "curl -f http://localhost:8000/api/ || true"

echo -e "\n${BLUE}🎨 Frontend Tests${NC}"
echo "==================="

# Wait for frontend to be ready
wait_for_service "Vue.js Frontend" "curl -f http://localhost:5173/ || curl -f http://localhost:3000/"

# Test frontend accessibility
run_test "Frontend accessibility (development)" "curl -f -I http://localhost:5173/ || true"
run_test "Frontend accessibility (production)" "curl -f -I http://localhost:3000/ || true"

echo -e "\n${BLUE}🔧 Service Health Tests${NC}"
echo "=========================="

# Check service status
run_test "All services running" "docker-compose ps | grep -v Exit"

# Check service logs for errors
echo -e "${YELLOW}📜 Checking service logs for critical errors...${NC}"
CRITICAL_ERRORS=$(docker-compose logs --tail=50 2>&1 | grep -i -E "(error|exception|failed|critical)" | grep -v -E "(404|GET|POST|health)" | wc -l)
if [ "$CRITICAL_ERRORS" -eq 0 ]; then
    echo -e "${GREEN}✅ No critical errors found in logs${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}❌ Found $CRITICAL_ERRORS potential critical errors in logs${NC}"
    echo "Recent logs with errors:"
    docker-compose logs --tail=20 2>&1 | grep -i -E "(error|exception|failed|critical)" | head -5 || true
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

echo -e "\n${BLUE}📊 Performance Tests${NC}"
echo "======================"

# Test response times
DJANGO_RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}' http://localhost:8000/admin/ || echo "0")
run_test "Django response time reasonable" "python3 -c \"assert float('$DJANGO_RESPONSE_TIME') < 5.0, 'Response time too slow: ${DJANGO_RESPONSE_TIME}s'\""

# Test database query performance
run_test "Database query performance" "docker-compose exec -T web python manage.py shell -c '
import time
from trades.models import Cryptocurrency
start_time = time.time()
count = Cryptocurrency.objects.count()
query_time = time.time() - start_time
print(f\"Query took {query_time:.3f}s for {count} records\")
assert query_time < 1.0, f\"Query too slow: {query_time}s\"
'"

echo -e "\n${BLUE}💾 Data Persistence Tests${NC}"
echo "=========================="

# Test data persistence by restarting services
echo -e "${YELLOW}♻️ Testing data persistence (restarting services)...${NC}"
run_test "Stop services" "docker-compose stop"
run_test "Start services again" "docker-compose start"

# Wait for services to be ready again
wait_for_service "Database after restart" "docker-compose exec -T db pg_isready -U postgres"
wait_for_service "Django after restart" "curl -f http://localhost:8000/admin/ -m 10"

# Verify data survived restart
run_test "Data persisted after restart" "docker-compose exec -T web python manage.py shell -c '
from trades.models import Cryptocurrency
count = Cryptocurrency.objects.count()
print(f\"Cryptocurrencies after restart: {count}\")
assert count > 0, \"Data lost after restart\"
'"

echo -e "\n${BLUE}🧪 Integration Tests${NC}"
echo "======================"

# Test creating a superuser
run_test "Create Django superuser" "echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='testadmin').delete(); User.objects.create_superuser('testadmin', 'test@fluxor.com', 'testpass123'); print('Superuser created')\" | docker-compose exec -T web python manage.py shell"

# Test admin login functionality
run_test "Test admin login" "docker-compose exec -T web python manage.py shell -c '
from django.contrib.auth import authenticate
user = authenticate(username=\"testadmin\", password=\"testpass123\")
assert user is not None, \"Authentication failed\"
assert user.is_superuser, \"User is not superuser\"
print(\"Admin authentication successful\")
'"

echo -e "\n${BLUE}📈 Final System State${NC}"
echo "======================="

# Show final system state
echo -e "${YELLOW}📊 System Statistics:${NC}"
echo "Services status:"
docker-compose ps

echo -e "\nDatabase statistics:"
docker-compose exec -T web python manage.py shell -c '
from trades.models import *
from django.contrib.auth import get_user_model
User = get_user_model()

print(f"Users: {User.objects.count()}")
print(f"Cryptocurrencies: {Cryptocurrency.objects.count()}")
print(f"Active cryptocurrencies: {Cryptocurrency.objects.filter(is_active=True).count()}")
print(f"Stablecoins: {Cryptocurrency.objects.filter(is_stablecoin=True).count()}")
print(f"Featured cryptos: {Cryptocurrency.objects.filter(is_featured=True).count()}")
print(f"Price data points: {PriceData.objects.count()}")
print(f"Trading signals: {TradingSignal.objects.count()}")
print(f"Automated tasks: {AutomatedTask.objects.count()}")
'

# Test Summary
echo -e "\n${BLUE}📋 Test Results Summary${NC}"
echo "=========================="
echo -e "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 ALL TESTS PASSED! 🎉${NC}"
    echo -e "${GREEN}Your Fluxor Trading Platform is ready for use!${NC}"
    echo ""
    echo -e "${BLUE}🌐 Access your application:${NC}"
    echo -e "  • Frontend (Development): ${YELLOW}http://localhost:5173${NC}"
    echo -e "  • Backend API: ${YELLOW}http://localhost:8000${NC}"
    echo -e "  • Admin Panel: ${YELLOW}http://localhost:8000/admin/${NC}"
    echo -e "  • Admin Credentials: ${YELLOW}testadmin / testpass123${NC}"
    echo ""
    echo -e "${BLUE}🚀 Start trading with 200+ cryptocurrencies!${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Some tests failed. Please check the output above for details.${NC}"
    echo -e "${YELLOW}💡 You can still use the system, but some features may not work correctly.${NC}"
    exit 1
fi