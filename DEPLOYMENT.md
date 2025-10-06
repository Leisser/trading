# 🚀 Fluxor Deployment Guide

This guide explains how to deploy the Fluxor trading platform to production.

## 📋 Prerequisites

- Docker and Docker Compose installed on your server
- Domain name configured to point to your server
- SSL certificate (recommended for production)
- Server with at least 4GB RAM and 2 CPU cores

## 🏗️ Architecture Overview

The Fluxor platform consists of:

- **Next.js Web App** (`web` service) - Main frontend application
- **Django API** (`api` service) - Backend API and business logic
- **PostgreSQL Database** (`db` service) - Data storage
- **Redis** (`redis` service) - Caching and message broker
- **Celery Workers** - Background task processing
- **Nginx** - Reverse proxy and load balancer
- **Dashboard** - Admin dashboard (optional)

## 🔧 Production Setup

### 1. Environment Configuration

Copy the environment template and configure your production settings:

```bash
cp env.production.example .env.production
```

Edit `.env.production` with your actual values:

```bash
# Database
POSTGRES_PASSWORD=your_secure_password_here
SECRET_KEY=your_django_secret_key_here

# Domain Configuration
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# API URLs
NEXT_PUBLIC_API_URL=https://your-domain.com/api
```

### 2. SSL Certificate Setup (Recommended)

For HTTPS, obtain an SSL certificate using Let's Encrypt:

```bash
# Install certbot
sudo apt install certbot

# Obtain certificate
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com
```

### 3. Deployment

Run the deployment script:

```bash
./deploy.sh
```

Or manually:

```bash
# Stop existing services
docker-compose -f docker-compose.prod.yml down

# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose -f docker-compose.prod.yml exec api python manage.py migrate

# Seed cryptocurrency data
docker-compose -f docker-compose.prod.yml exec api python manage.py seed_cryptocurrencies --file=cryptocurrency_data_complete.json --update

# Collect static files
docker-compose -f docker-compose.prod.yml exec api python manage.py collectstatic --noinput
```

## 🌐 Service URLs

After deployment, your services will be available at:

- **Main Website**: `https://your-domain.com:5173`
- **API**: `https://your-domain.com:8000/api`
- **Dashboard**: `https://your-domain.com:3001`
- **Database Admin**: `https://your-domain.com:5050` (pgAdmin)

## 🔄 GitHub Actions Deployment

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that:

1. Runs tests on every push
2. Builds the Next.js application
3. Can be configured to deploy to your server

To enable automatic deployment:

1. Add your server credentials to GitHub Secrets
2. Update the deployment step in the workflow
3. Configure your server to accept deployments

## 📊 Monitoring and Maintenance

### Health Checks

Check service status:

```bash
docker-compose -f docker-compose.prod.yml ps
```

### Logs

View service logs:

```bash
# All services
docker-compose -f docker-compose.prod.yml logs

# Specific service
docker-compose -f docker-compose.prod.yml logs web
docker-compose -f docker-compose.prod.yml logs api
```

### Database Management

Access the database:

```bash
docker-compose -f docker-compose.prod.yml exec db psql -U fluxor -d fluxor_prod
```

### Backup

Create database backup:

```bash
docker-compose -f docker-compose.prod.yml exec db pg_dump -U fluxor fluxor_prod > backup_$(date +%Y%m%d_%H%M%S).sql
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 80, 443, 5173, 8000, 3001, 5050 are available
2. **Permission Issues**: Ensure Docker has proper permissions
3. **SSL Issues**: Verify certificate paths and permissions
4. **Database Connection**: Check database credentials and network connectivity

### Service Restart

Restart specific services:

```bash
docker-compose -f docker-compose.prod.yml restart web
docker-compose -f docker-compose.prod.yml restart api
```

### Complete Rebuild

If you need to completely rebuild:

```bash
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
```

## 🔒 Security Considerations

1. **Environment Variables**: Never commit `.env.production` to version control
2. **Database Passwords**: Use strong, unique passwords
3. **SSL/TLS**: Always use HTTPS in production
4. **Firewall**: Configure firewall to only allow necessary ports
5. **Updates**: Regularly update Docker images and dependencies

## 📈 Scaling

For high-traffic scenarios:

1. **Load Balancing**: Use multiple API instances
2. **Database**: Consider read replicas
3. **Caching**: Implement Redis clustering
4. **CDN**: Use a CDN for static assets

## 🆘 Support

If you encounter issues:

1. Check the logs: `docker-compose -f docker-compose.prod.yml logs`
2. Verify environment variables
3. Ensure all services are healthy
4. Check network connectivity between services
