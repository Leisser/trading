# Fluxor Trading Platform

A comprehensive financial trading platform with Django backend, Vue.js frontend with admin dashboard, and automated trading tasks.

## 🏗️ Architecture

- **Backend**: Django REST API with PostgreSQL database
- **Frontend**: Vue.js with Vite (includes admin dashboard)
- **Task Queue**: Celery with Redis broker
- **Proxy**: Nginx reverse proxy
- **Containerization**: Docker Compose orchestration

## 🚀 Quick Start

### Development Mode

```bash
# Start all services in development mode
./start-dev.sh

# Or manually:
docker-compose up --build -d
```

**Available at:**
- Frontend: http://localhost:5173 (Vite dev server with hot reload)
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin/

### Production Mode

```bash
# Start all services in production mode
./start-prod.sh

# Or manually:
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

**Available at:**
- Frontend: http://localhost:3000 (optimized build)
- Backend API: http://localhost:8000
- Nginx Proxy: http://localhost:80

## 📦 Services

### Core Services
- **db**: PostgreSQL 15 database
- **redis**: Redis cache and message broker
- **web**: Django application server
- **frontend**: Vue.js application with admin dashboard

### Background Services
- **celery_worker**: Celery task worker
- **celery_beat**: Celery task scheduler
- **trading_tasks**: Automated financial data updates (development only)
- **nginx**: Reverse proxy and static file server

## 🛠️ Management Commands

### Service Management
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service_name]

# Rebuild specific service
docker-compose build [service_name]

# Execute commands in containers
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Development Commands
```bash
# Install frontend dependencies
docker-compose exec frontend npm install

# Run Django migrations
docker-compose exec web python manage.py migrate

# Create Django superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec api python manage.py test admin_control.tests investments.tests strategy_engine.tests core.tests dashboard.tests fluxor_api.tests --verbosity=1
docker-compose exec frontend npm test
```

## 🗂️ Project Structure

```
fluxor_api/
├── fluxor_api/              # Django project settings
├── src/                     # Vue.js frontend application
│   ├── components/          # Vue components
│   ├── views/              # Vue pages/views
│   ├── router/             # Vue router configuration
│   ├── assets/             # Static assets
│   └── Dockerfile          # Frontend container definition
├── trading/                 # Django trading app
├── management/              # Django management commands
├── Dockerfile              # Backend container definition
└── requirements.txt        # Python dependencies
```

## 🔧 Configuration

### Environment Variables

**Django (Backend)**
- `DJANGO_SETTINGS_MODULE`: Django settings module
- `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Database configuration
- `REDIS_URL`: Redis connection string
- `CORS_ALLOWED_ORIGINS`: Frontend origins for CORS

**Vue.js (Frontend)**
- `VITE_API_URL`: Backend API base URL
- `VITE_WS_URL`: WebSocket connection URL
- `NODE_ENV`: Environment mode (development/production)

### Database Setup

The PostgreSQL database is automatically initialized with:
- Database: `fluxor_api`
- Username: `postgres`
- Password: `postgres`
- Port: `5432`

### Redis Configuration

Redis is configured as:
- Host: `redis`
- Port: `6379`
- Database: `0`

## 🔄 Automated Trading Tasks

The platform includes automated financial data updates:

- **Development**: Runs as separate `trading_tasks` service
- **Production**: Managed by Celery Beat scheduler
- **Interval**: Configurable (default: 1 minute)
- **Tasks**: Market data updates, portfolio calculations, risk assessments

## 🧪 Testing

### Backend Tests
```bash
docker-compose exec api python manage.py test admin_control.tests investments.tests strategy_engine.tests core.tests dashboard.tests fluxor_api.tests --verbosity=1
```

### Frontend Tests
```bash
docker-compose exec frontend npm test
```

### Integration Tests
```bash
# Run all tests
docker-compose exec api python manage.py test admin_control.tests investments.tests strategy_engine.tests core.tests dashboard.tests fluxor_api.tests --verbosity=1
docker-compose exec frontend npm run test:unit
```

## 🔒 Security

### Production Security
- Non-root users in containers
- Health checks for all services
- Environment-specific configurations
- Static file serving via Nginx
- Database and Redis data persistence

### Development Security
- CORS configured for local development
- Debug mode enabled
- Volume mounts for hot reloading

## 📊 Monitoring

### Health Checks
All services include health checks:
- Database: `pg_isready`
- Redis: `redis-cli ping`
- Django: HTTP health endpoint
- Frontend: HTTP availability check

### Logging
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f celery_worker
docker-compose logs -f trading_tasks
```

## 🚨 Troubleshooting

### Common Issues

**Port Conflicts**
```bash
# Check what's using ports
lsof -i :8000  # Django
lsof -i :3000  # Frontend (production)
lsof -i :5173  # Frontend (development)
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
```

**Database Issues**
```bash
# Reset database
docker-compose down -v
docker-compose up -d db
docker-compose exec web python manage.py migrate
```

**Permission Issues**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

**Container Issues**
```bash
# Rebuild all containers
docker-compose build --no-cache

# Remove all containers and start fresh
docker-compose down -v
docker system prune -a
docker-compose up --build -d
```

## 📈 Scaling

### Production Scaling
```bash
# Scale Celery workers
docker-compose up -d --scale celery_worker=3

# Scale web servers (with load balancer)
docker-compose up -d --scale web=2
```

### Resource Monitoring
```bash
# Monitor container resources
docker stats

# Monitor specific container
docker stats trading_web_1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes in development mode
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎯 Next Steps

After setup:
1. Visit the admin dashboard at http://localhost:5173
2. Configure your trading parameters
3. Set up API keys for data providers
4. Customize trading strategies
5. Monitor automated tasks in the admin panel