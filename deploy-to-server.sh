#!/bin/bash

# Fluxor Trading Platform - Production Deployment Script
# Server: 31.97.103.64

set -e

echo "🚀 Fluxor Trading Platform - Production Deployment"
echo "================================================="
echo "Server: 31.97.103.64"
echo ""

# Configuration
SERVER_IP="31.97.103.64"
SERVER_USER="root"
PROJECT_DIR="/opt/fluxor"
BACKUP_DIR="/opt/fluxor-backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on server
if [ "$(hostname -I | awk '{print $1}')" != "$SERVER_IP" ]; then
    log_error "This script should be run on the production server (31.97.103.64)"
    exit 1
fi

log_info "Starting deployment on server $SERVER_IP..."

# Create backup directory
log_info "Creating backup directory..."
mkdir -p $BACKUP_DIR

# Create project directory
log_info "Creating project directory..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Clone or update repository
if [ -d ".git" ]; then
    log_info "Updating existing repository..."
    git pull origin main
else
    log_info "Cloning repository..."
    git clone https://github.com/Leisser/trading.git .
fi

# Create backup of current deployment
log_info "Creating backup of current deployment..."
if [ -d "$PROJECT_DIR" ]; then
    tar -czf "$BACKUP_DIR/fluxor_backup_$DATE.tar.gz" \
        --exclude='node_modules' \
        --exclude='.git' \
        --exclude='*.log' \
        .
    log_success "Backup created: $BACKUP_DIR/fluxor_backup_$DATE.tar.gz"
fi

# Copy production environment
log_info "Setting up production environment..."
cp env.production .env

# Update environment variables with server IP
log_info "Updating environment variables..."
sed -i "s/YOUR_SERVER_IP/$SERVER_IP/g" .env

# Install Docker and Docker Compose if not present
log_info "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    log_info "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
fi

if ! command -v docker-compose &> /dev/null; then
    log_info "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Stop existing containers
log_info "Stopping existing containers..."
docker-compose down || true

# Remove old containers and images
log_info "Cleaning up old containers and images..."
docker system prune -f || true

# Build and start services
log_info "Building and starting services..."
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to be ready
log_info "Waiting for services to be ready..."
sleep 30

# Check service health
log_info "Checking service health..."
docker-compose ps

# Test endpoints
log_info "Testing endpoints..."
echo "Testing main application..."
curl -f http://localhost/health/ || log_warning "Main app health check failed"

echo "Testing API..."
curl -f http://localhost/api/health/ || log_warning "API health check failed"

# Setup SSL certificates (if certbot is available)
if command -v certbot &> /dev/null; then
    log_info "Setting up SSL certificates..."
    certbot certonly --nginx -d fluxor.pro -d www.fluxor.pro -d api.fluxor.pro -d dashboard.fluxor.pro -d db.fluxor.pro --non-interactive --agree-tos --email admin@fluxor.pro || log_warning "SSL certificate setup failed"
else
    log_warning "Certbot not found. SSL certificates need to be set up manually."
fi

# Setup firewall
log_info "Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Setup log rotation
log_info "Setting up log rotation..."
cat > /etc/logrotate.d/fluxor << EOF
/var/log/nginx/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        docker-compose -f $PROJECT_DIR/docker-compose.prod.yml exec nginx nginx -s reload
    endscript
}
EOF

# Setup monitoring
log_info "Setting up basic monitoring..."
cat > /opt/fluxor/monitor.sh << 'EOF'
#!/bin/bash
# Basic health monitoring script

PROJECT_DIR="/opt/fluxor"
cd $PROJECT_DIR

# Check if containers are running
if ! docker-compose ps | grep -q "Up"; then
    echo "$(date): Some containers are down" >> /var/log/fluxor-monitor.log
    # Restart containers
    docker-compose up -d
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "$(date): Disk usage is high: ${DISK_USAGE}%" >> /var/log/fluxor-monitor.log
fi
EOF

chmod +x /opt/fluxor/monitor.sh

# Add to crontab for monitoring
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/fluxor/monitor.sh") | crontab -

log_success "Deployment completed successfully!"
echo ""
echo "🌐 Your Fluxor Trading Platform is now live at:"
echo "=============================================="
echo "Main App:     http://fluxor.pro"
echo "API:          http://api.fluxor.pro"
echo "Dashboard:    http://dashboard.fluxor.pro"
echo "Database:     http://db.fluxor.pro"
echo ""
echo "📊 Management Commands:"
echo "======================"
echo "View logs:    docker-compose -f $PROJECT_DIR/docker-compose.prod.yml logs -f"
echo "Restart:      docker-compose -f $PROJECT_DIR/docker-compose.prod.yml restart"
echo "Stop:        docker-compose -f $PROJECT_DIR/docker-compose.prod.yml down"
echo "Update:       cd $PROJECT_DIR && git pull && docker-compose -f docker-compose.prod.yml up -d --build"
echo ""
echo "🔧 Next Steps:"
echo "=============="
echo "1. Configure DNS records to point to $SERVER_IP"
echo "2. Set up SSL certificates with Let's Encrypt"
echo "3. Configure your domain provider"
echo "4. Test all endpoints"
echo ""
log_success "Fluxor Trading Platform deployment complete! 🎉"
