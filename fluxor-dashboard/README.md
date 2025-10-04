# Fluxor Dashboard

A comprehensive admin dashboard for the Fluxor cryptocurrency trading platform, built with Vue 3, TypeScript, and Tailwind CSS.

## 🌟 Features

### Current Features
- **Modern Dashboard Layout**: Clean, responsive admin interface with sidebar navigation
- **Cryptocurrency Management**: Full CRUD operations for managing 200+ cryptocurrencies
  - Advanced filtering and search
  - Bulk operations
  - Real-time price updates
  - Import functionality
- **Interactive Charts**: Trading volume and performance visualizations
- **User-Friendly Interface**: Intuitive design with Tailwind CSS styling
- **TypeScript Support**: Type-safe development environment
- **API Integration**: Ready to connect with Django backend

### Upcoming Features
- **User Management**: Complete user administration panel
- **Trading Dashboard**: Real-time trading interface
- **Reports System**: Comprehensive reporting and analytics
- **Security Panel**: Security monitoring and settings
- **System Configuration**: Advanced system settings

## 🚀 Quick Start

### Development Mode

```bash
# Navigate to dashboard directory
cd fluxor-dashboard

# Install dependencies
npm install

# Start development server
npm run dev
# or
./dev.sh

# Open browser to http://localhost:5173
```

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Docker Deployment

The dashboard is integrated into the main Docker Compose setup:

```bash
# From the main trading directory
docker-compose up dashboard

# Access at http://localhost:3001
```

## 🛠️ Technology Stack

- **Vue 3**: Progressive JavaScript framework
- **TypeScript**: Type-safe JavaScript development
- **Tailwind CSS**: Utility-first CSS framework
- **Vue Router**: Official routing library
- **Pinia**: State management (ready for implementation)
- **Axios**: HTTP client for API calls
- **Heroicons**: Beautiful SVG icons
- **Headless UI**: Unstyled, accessible UI components
- **Chart.js**: Charting library (ready for implementation)
- **Vite**: Fast build tool and development server

## 🔌 API Integration

The dashboard is designed to work with the Django backend API:

```typescript
// Example API usage
import { api } from '@/services/api'

// Get cryptocurrencies
const cryptos = await api.cryptocurrencies.getAll({
  page: 1,
  page_size: 50,
  search: 'bitcoin'
})

// Update cryptocurrency
await api.cryptocurrencies.update(id, {
  is_active: true,
  is_featured: true
})
```

### Environment Configuration

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api

# Application Settings
VITE_APP_NAME=Fluxor Dashboard
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_TRADING=true
VITE_ENABLE_REPORTS=true
VITE_ENABLE_SECURITY=true
```

## 🐳 Docker Integration

The dashboard integrates seamlessly with the existing Docker Compose setup:

```yaml
dashboard:
  build:
    context: ./fluxor-dashboard
    dockerfile: Dockerfile
  ports:
    - "3001:80"
  environment:
    - VITE_API_BASE_URL=http://localhost:8000/api
    - NODE_ENV=production
```

## 🔧 Development

### Prerequisites
- Node.js 18+ (recommended: 20+)
- npm 8+
- Docker (for containerized development)

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run type-check` - TypeScript type checking
- `npm run lint` - ESLint code linting
- `npm run format` - Prettier code formatting

## 🚢 Deployment

### Production Build
```bash
npm run build
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up dashboard

# Access at http://localhost:3001
```

## 📝 License

This project is part of the Fluxor trading platform.