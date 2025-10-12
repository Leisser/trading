# Fluxor Trading Platform - Complete Setup Guide

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git installed
- Python 3.9+ (for testing scripts)

### 1. Clone and Start Services
```bash
# Clone the repository
git clone https://github.com/Leisser/trading.git
cd trading

# Start all services
docker-compose up -d

# Wait for services to be healthy (about 30 seconds)
docker-compose ps
```

### 2. Access the Applications
- **Main Website**: http://localhost:5173
- **Admin Dashboard**: http://localhost:3001
- **API Documentation**: http://localhost:8000/swagger/
- **Database Admin**: http://localhost:5050 (pgAdmin)

## 🏗️ Architecture Overview

### Services
1. **PostgreSQL Database** (port 5432)
2. **Redis Cache** (port 6379)
3. **Django API** (port 8000)
4. **Next.js Web App** (port 5173)
5. **Vue.js Dashboard** (port 3001)
6. **Nginx Proxy** (port 80/443)

### Authentication Flow
```
User Registration → Email/Password → JWT Tokens → Protected Access
```

## 📋 Step-by-Step Setup

### 1. Environment Configuration
The project uses the existing `.env` file with proper configuration:
```bash
# Database
DB_HOST=db
DB_NAME=fluxor_api
DB_USER=postgres
DB_PASSWORD=postgres

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:80,http://localhost:8000
```

### 2. Start Database Services
```bash
# Start PostgreSQL and Redis
docker-compose up -d db redis

# Verify they're running
docker-compose ps
```

### 3. Initialize Database
```bash
# Run migrations
docker-compose run --rm api python manage.py migrate

# Create superuser (optional)
docker-compose run --rm api python manage.py createsuperuser --username admin --email admin@fluxor.pro --noinput

# Set admin password
docker-compose run --rm api python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
admin = User.objects.get(username='admin');
admin.set_password('admin123');
admin.save();
print('Admin password set to: admin123')
"

# Collect static files
docker-compose run --rm api python manage.py collectstatic --noinput
```

### 4. Start All Services
```bash
# Start API
docker-compose up -d api

# Start Web Application
docker-compose up -d web

# Start Dashboard
docker-compose up -d dashboard

# Verify all services are running
docker-compose ps
```

## 🧪 Testing the Setup

### Automated Test
```bash
# Install Python requests library
pip3 install requests

# Run comprehensive test
python3 test-auth-flow.py
```

### Manual Testing

#### 1. Test Registration
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "confirm_password": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

#### 2. Test Sign-In
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test@example.com",
    "password": "testpassword123"
  }'
```

#### 3. Test Protected Endpoint
```bash
# Use the access token from sign-in response
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/profile/
```

## 🌐 Web Interface Testing

### 1. Registration Flow
1. Visit http://localhost:5173/signup
2. Fill in the registration form
3. Submit and verify success message

### 2. Sign-In Flow
1. Visit http://localhost:5173/signin
2. Use registered credentials
3. Verify successful authentication

### 3. Dashboard Access
1. Visit http://localhost:3001
2. View admin dashboard
3. Check statistics and functionality

## 🔧 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check what's using ports
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
lsof -i :8000  # API
lsof -i :5173  # Web
lsof -i :3001  # Dashboard

# Stop conflicting services
docker stop <container_name>
```

#### Database Connection Issues
```bash
# Check database status
docker-compose exec db psql -U postgres -d fluxor_api -c "SELECT version();"

# Reset database if needed
docker-compose down -v
docker-compose up -d db redis
# Re-run migrations
```

#### API Not Responding
```bash
# Check API logs
docker-compose logs api

# Restart API service
docker-compose restart api
```

### Service Health Checks
```bash
# Check all services
docker-compose ps

# Test API health
curl http://localhost:8000/api/health/

# Test web accessibility
curl -I http://localhost:5173/

# Test dashboard
curl -I http://localhost:3001/
```

## 📊 Default Credentials

### Admin User
- **Username**: admin
- **Email**: admin@fluxor.pro
- **Password**: admin123

### Database
- **Host**: localhost:5432
- **Database**: fluxor_api
- **Username**: postgres
- **Password**: postgres

### pgAdmin (Database Management)
- **URL**: http://localhost:5050
- **Email**: admin@fluxor.pro
- **Password**: admin123

## 🔒 Security Notes

### Development Environment
- Default passwords are used for development
- CORS is configured for local development
- Debug mode is enabled

### Production Deployment
- Change all default passwords
- Configure proper environment variables
- Enable SSL/TLS
- Set up proper CORS policies
- Disable debug mode

## 📈 Performance Optimization

### Development
- Services start in development mode
- Hot reloading enabled for web applications
- Debug logging enabled

### Production
- Use production Docker compose file
- Enable caching
- Configure CDN for static files
- Set up load balancing

## 🎯 Next Steps

1. **Immediate Use**: System is ready for development and testing
2. **Firebase OAuth**: Configure for social login (optional)
3. **Production**: Deploy using production configuration
4. **Monitoring**: Add logging and monitoring tools
5. **Security**: Implement additional security measures

## 📞 Support

For issues or questions:
1. Check the logs: `docker-compose logs <service_name>`
2. Verify environment variables
3. Review this documentation
4. Check the AUTHENTICATION_STATUS.md file for detailed status
