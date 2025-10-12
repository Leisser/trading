#!/bin/bash

# Fluxor Trading Platform Startup Script
# This script sets up and starts the complete Fluxor trading platform

set -e

echo "🚀 Starting Fluxor Trading Platform..."
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_status "Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose is not installed. Please install it and try again."
    exit 1
fi

print_status "Docker Compose is available"

# Stop any existing services
print_info "Stopping any existing services..."
docker-compose down > /dev/null 2>&1 || true

# Start database services first
print_info "Starting database services..."
docker-compose up -d db redis

# Wait for databases to be healthy
print_info "Waiting for databases to be ready..."
sleep 10

# Check database health
if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then
    print_status "PostgreSQL is ready"
else
    print_error "PostgreSQL failed to start"
    exit 1
fi

if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    print_status "Redis is ready"
else
    print_error "Redis failed to start"
    exit 1
fi

# Run database migrations
print_info "Running database migrations..."
docker-compose run --rm api python manage.py migrate > /dev/null 2>&1

# Create superuser if it doesn't exist
print_info "Setting up admin user..."
docker-compose run --rm api python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@fluxor.pro', 'admin123');
    print('Admin user created');
else:
    print('Admin user already exists');
" > /dev/null 2>&1

# Collect static files
print_info "Collecting static files..."
docker-compose run --rm api python manage.py collectstatic --noinput > /dev/null 2>&1

# Start API service
print_info "Starting API service..."
docker-compose up -d api

# Wait for API to be ready
print_info "Waiting for API to be ready..."
sleep 15

# Check API health
if curl -s http://localhost:8000/api/health/ > /dev/null 2>&1; then
    print_status "API is ready"
else
    print_error "API failed to start"
    exit 1
fi

# Start web application
print_info "Starting web application..."
docker-compose up -d web

# Start dashboard
print_info "Starting dashboard..."
docker-compose up -d dashboard

# Wait for services to be ready
print_info "Waiting for all services to be ready..."
sleep 10

# Check all services
print_info "Checking service status..."

# Check web application
if curl -s -I http://localhost:5173/ | grep -q "200 OK"; then
    print_status "Web application is ready"
else
    print_warning "Web application may still be starting..."
fi

# Check dashboard
if curl -s -I http://localhost:3001/ | grep -q "200 OK"; then
    print_status "Dashboard is ready"
else
    print_warning "Dashboard may still be starting..."
fi

# Show service status
echo ""
print_info "Service Status:"
docker-compose ps

echo ""
print_status "Fluxor Trading Platform is now running!"
echo ""
echo "🌐 Access URLs:"
echo "   Main Website:    http://localhost:5173"
echo "   Admin Dashboard: http://localhost:3001"
echo "   API Docs:        http://localhost:8000/swagger/"
echo "   Database Admin:  http://localhost:5050"
echo ""
echo "🔐 Default Credentials:"
echo "   Admin Username:  admin"
echo "   Admin Password:  admin123"
echo ""
echo "📚 Documentation:"
echo "   Setup Guide:     ./SETUP_GUIDE.md"
echo "   Auth Status:     ./AUTHENTICATION_STATUS.md"
echo ""
echo "🧪 Test the system:"
echo "   pip3 install requests && python3 test-auth-flow.py"
echo ""
print_status "Setup complete! Happy trading! 🚀"
