# Fluxor Production Deployment Guide

This guide covers deploying the Fluxor trading platform to production using Docker and GitHub Actions.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Dashboard     │    │   Nginx Proxy   │
│   (Vue.js)      │    │   (Vue.js)      │    │   (Port 80)     │
│   Port 5173     │    │   Port 3001     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Django API    │
                    │   (Port 8000)   │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │     Redis       │    │   Celery        │
│   (Port 5432)   │    │   (Port 6379)   │    │   Workers       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Server Setup

```bash
# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone https://github.com/your-username/fluxor.git /opt/fluxor
cd /opt/fluxor
```

### 2. Environment Configuration

```bash
# Copy production environment template
cp env.production .env

# Edit environment variables
nano .env
```

**Required Environment Variables:**
- `POSTGRES_PASSWORD`: Secure database password
- `SECRET_KEY`: Django secret key (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `ALLOWED_HOSTS`: Your domain name
- `CORS_ALLOWED_ORIGINS`: Your frontend URLs

### 3. Deploy

```bash
# Run deployment script
./deploy.sh
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

#### 1. Continuous Integration (`ci.yml`)
- **Triggers**: Push to `main`/`develop`, Pull Requests
- **Tests**: Python tests, Frontend tests, Linting, Security scans
- **Build**: Docker images, Frontend/Dashboard builds
- **Validation**: Docker container health checks

#### 2. Production Deployment (`deploy.yml`)
- **Triggers**: Push to `main` branch
- **Process**: 
  1. Build and push Docker images to GitHub Container Registry
  2. Deploy to production server via SSH
  3. Run migrations and collect static files
  4. Health checks and notifications

### Required GitHub Secrets

Add these secrets to your GitHub repository:

```
SERVER_HOST=your-server-ip
SERVER_USER=your-username
SERVER_SSH_KEY=your-private-ssh-key
SLACK_WEBHOOK=your-slack-webhook-url (optional)
```

## 🐳 Docker Configuration

### Production Docker Compose (`docker-compose.prod.yml`)

**Services:**
- **web**: Django API with Gunicorn
- **frontend**: Vue.js frontend (Nginx)
- **dashboard**: Vue.js dashboard (Nginx)
- **nginx**: Reverse proxy and load balancer
- **db**: PostgreSQL database
- **redis**: Redis cache and message broker
- **celery_worker**: Background task processing
- **celery_beat**: Scheduled task management
- **trading_tasks**: Trading engine tasks

**Features:**
- Health checks for all services
- Automatic restarts on failure
- Volume persistence for data
- Network isolation
- Resource limits

### Nginx Configuration (`nginx.prod.conf`)

**Features:**
- Reverse proxy for all services
- SSL/TLS termination
- Rate limiting
- Security headers
- Gzip compression
- Static file serving
- WebSocket support

## 📊 Monitoring & Maintenance

### Health Checks

```bash
# Check all services
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Check specific service
docker-compose -f docker-compose.prod.yml logs web
```

### Database Management

```bash
# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Backup database
docker-compose -f docker-compose.prod.yml exec db pg_dump -U fluxor fluxor_prod > backup.sql
```

### Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

## 🔒 Security Considerations

### Environment Security
- Use strong passwords for database and Django secret key
- Enable SSL/TLS certificates
- Configure firewall rules
- Regular security updates

### Application Security
- CORS configuration
- Rate limiting
- Security headers
- Input validation
- Authentication and authorization

### Infrastructure Security
- Container security scanning
- Network isolation
- Volume encryption
- Backup encryption

## 📈 Performance Optimization

### Database
- Connection pooling
- Query optimization
- Indexing
- Regular maintenance

### Caching
- Redis configuration
- Application-level caching
- Static file caching
- CDN integration

### Monitoring
- Application metrics
- System metrics
- Log aggregation
- Alerting

## 🆘 Troubleshooting

### Common Issues

**1. Services not starting:**
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check resource usage
docker stats
```

**2. Database connection issues:**
```bash
# Check database status
docker-compose -f docker-compose.prod.yml exec db pg_isready

# Check environment variables
docker-compose -f docker-compose.prod.yml exec web env | grep DATABASE
```

**3. Frontend not loading:**
```bash
# Check nginx configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

# Check static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic
```

### Log Locations
- Application logs: `docker-compose -f docker-compose.prod.yml logs`
- Nginx logs: `/var/log/nginx/`
- System logs: `/var/log/syslog`

## 📞 Support

For deployment issues:
1. Check the logs: `docker-compose -f docker-compose.prod.yml logs`
2. Verify environment variables
3. Check GitHub Actions workflow status
4. Review this documentation

## 🔄 Backup Strategy

### Automated Backups
- Database backups before each deployment
- Configuration backups
- Volume snapshots

### Manual Backups
```bash
# Database backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U fluxor fluxor_prod > backup_$(date +%Y%m%d).sql

# Full system backup
tar -czf fluxor_backup_$(date +%Y%m%d).tar.gz /opt/fluxor
```

This deployment setup provides a robust, scalable, and maintainable production environment for the Fluxor trading platform.
