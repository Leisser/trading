#!/bin/bash

# Fluxor Dashboard Development Script

echo "🚀 Starting Fluxor Dashboard Development Environment"
echo "================================================="

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating environment file..."
    cp .env.example .env
fi

# Start development server
echo "🌟 Starting development server..."
echo "Dashboard will be available at: http://localhost:5173"
echo "API backend should be running at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev