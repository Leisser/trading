#!/bin/bash

# Development startup script for Fluxor Trading Platform
set -e

echo "🚀 Starting Fluxor Trading Platform in Development Mode..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p fluxor_api/logs
mkdir -p fluxor_api/media
mkdir -p ssl

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ Development environment is ready!"
echo ""
echo "🌐 Services available at:"
echo "   • Frontend (Vue.js + Admin Dashboard): http://localhost:5173"
echo "   • Backend API (Django): http://localhost:8000"
echo "   • Admin Panel: http://localhost:8000/admin/"
echo "   • PostgreSQL Database: localhost:5432"
echo "   • Redis Cache: localhost:6379"
echo "   • Nginx Proxy: http://localhost:80"
echo ""
echo "📊 Trading tasks are running automatically in the background"
echo ""
echo "🛑 To stop all services: docker-compose down"
echo "📜 To view logs: docker-compose logs -f [service_name]"