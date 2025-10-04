#!/bin/bash

# Production Deployment Script
# This script should be run on the production server

set -e

echo "🚀 Starting Fluxor Production Deployment..."

# Configuration
PROJECT_DIR="/opt/fluxor"
BACKUP_DIR="/opt/fluxor-backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   log_error "This script should not be run as root"
   exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Navigate to project directory
cd $PROJECT_DIR

# Create backup of current deployment
log_info "Creating backup of current deployment..."
if [ -d "$PROJECT_DIR" ]; then
    tar -czf "$BACKUP_DIR/fluxor_backup_$DATE.tar.gz" \
        --exclude='node_modules' \
        --exclude='.git' \
        --exclude='*.log' \
        .
    log_info "Backup created: $BACKUP_DIR/fluxor_backup_$DATE.tar.gz"
fi

# Pull latest code
log_info "Pulling latest code from Git..."
git fetch origin
git reset --hard origin/main

# Stop existing containers
log_info "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down || true

# Pull latest images
log_info "Pulling latest Docker images..."
docker-compose -f docker-compose.prod.yml pull

# Build new images
log_info "Building Docker images..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Start services
log_info "Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for database to be ready
log_info "Waiting for database to be ready..."
sleep 30

# Run database migrations
log_info "Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate

# Collect static files
log_info "Collecting static files..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
log_info "Creating superuser if needed..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
" || true

# Restart services to ensure everything is running
log_info "Restarting services..."
docker-compose -f docker-compose.prod.yml restart

# Health checks
log_info "Performing health checks..."
sleep 30

# Check API health
if curl -f http://localhost:8000/api/health/ > /dev/null 2>&1; then
    log_info "✅ API health check passed"
else
    log_error "❌ API health check failed"
    exit 1
fi

# Check Frontend
if curl -f http://localhost:5173/ > /dev/null 2>&1; then
    log_info "✅ Frontend health check passed"
else
    log_error "❌ Frontend health check failed"
    exit 1
fi

# Check Dashboard
if curl -f http://localhost:3001/ > /dev/null 2>&1; then
    log_info "✅ Dashboard health check passed"
else
    log_error "❌ Dashboard health check failed"
    exit 1
fi

# Clean up old Docker images
log_info "Cleaning up old Docker images..."
docker image prune -f

# Show running containers
log_info "Current running containers:"
docker-compose -f docker-compose.prod.yml ps

# Show logs for any failed containers
log_info "Checking for any failed containers..."
FAILED_CONTAINERS=$(docker-compose -f docker-compose.prod.yml ps --services --filter "status=exited")
if [ ! -z "$FAILED_CONTAINERS" ]; then
    log_warn "Some containers have exited:"
    echo "$FAILED_CONTAINERS"
    log_info "Showing logs for failed containers:"
    for container in $FAILED_CONTAINERS; do
        echo "=== Logs for $container ==="
        docker-compose -f docker-compose.prod.yml logs $container
    done
fi

log_info "🎉 Deployment completed successfully!"
log_info "Services available at:"
log_info "  - API: http://localhost:8000/api/"
log_info "  - Frontend: http://localhost:5173/"
log_info "  - Dashboard: http://localhost:3001/"
log_info "  - Main Site: http://localhost/"

# Optional: Send notification
if [ ! -z "$SLACK_WEBHOOK" ]; then
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"🚀 Fluxor deployment completed successfully!\"}" \
        $SLACK_WEBHOOK
fi
