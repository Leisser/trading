#!/bin/bash

# Production startup script for Fluxor Trading Platform
set -e

echo "🚀 Starting Fluxor Trading Platform in Production Mode..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p fluxor_api/logs
mkdir -p fluxor_api/media
mkdir -p ssl

# Build and start services with production overrides
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 15

# Run Django migrations and collect static files
echo "🔄 Running database migrations..."
docker-compose exec web python manage.py migrate

echo "📦 Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

# Create Django superuser (if needed)
echo "👤 Creating superuser (if needed)..."
docker-compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fluxor.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ Production environment is ready!"
echo ""
echo "🌐 Services available at:"
echo "   • Frontend (Vue.js + Admin Dashboard): http://localhost:3000"
echo "   • Backend API (Django): http://localhost:8000"
echo "   • Admin Panel: http://localhost:8000/admin/"
echo "   • Nginx Proxy: http://localhost:80"
echo ""
echo "🔑 Default admin credentials: admin / admin123"
echo "📊 Trading tasks managed by Celery Beat scheduler"
echo ""
echo "🛑 To stop all services: docker-compose -f docker-compose.yml -f docker-compose.prod.yml down"
echo "📜 To view logs: docker-compose logs -f [service_name]"