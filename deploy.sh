#!/bin/bash

# Fluxor Production Deployment Script
# This script handles the deployment of the Fluxor trading platform

set -e  # Exit on any error

echo "🚀 Starting Fluxor deployment..."

# Check if we're in the right directory
if [ ! -f "docker-compose.prod.yml" ]; then
    echo "❌ Error: docker-compose.prod.yml not found. Please run this script from the project root."
    exit 1
fi

# Load environment variables
if [ -f ".env.production" ]; then
    echo "📋 Loading production environment variables..."
    export $(cat .env.production | grep -v '^#' | xargs)
else
    echo "⚠️  Warning: .env.production not found. Using default values."
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

# Pull latest images (if using remote registry)
echo "📥 Pulling latest images..."
docker-compose -f docker-compose.prod.yml pull

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose -f docker-compose.prod.yml exec api python manage.py migrate

# Seed cryptocurrency data (if needed)
echo "💰 Seeding cryptocurrency data..."
docker-compose -f docker-compose.prod.yml exec api python manage.py seed_cryptocurrencies --file=cryptocurrency_data_complete.json --update

# Collect static files
echo "📁 Collecting static files..."
docker-compose -f docker-compose.prod.yml exec api python manage.py collectstatic --noinput

# Restart services to ensure everything is working
echo "🔄 Restarting services..."
docker-compose -f docker-compose.prod.yml restart

# Check service health
echo "🏥 Checking service health..."
docker-compose -f docker-compose.prod.yml ps

echo "✅ Deployment completed successfully!"
echo "🌐 Your Next.js application should be available at: http://your-domain:5173"
echo "🔧 API should be available at: http://your-domain:8000/api"
echo "📊 Dashboard should be available at: http://your-domain:3001"