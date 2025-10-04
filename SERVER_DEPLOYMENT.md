# 🚀 Fluxor Trading Platform - Server Deployment Guide

## **Server Information**
- **IP Address**: `31.97.103.64`
- **Domain**: `fluxor.pro`
- **Subdomains**: `api.fluxor.pro`, `dashboard.fluxor.pro`, `db.fluxor.pro`

## **Quick Deployment Steps**

### **1. Connect to Your Server**
```bash
ssh root@31.97.103.64
```

### **2. Run the Deployment Script**
```bash
# Download and run the deployment script
curl -fsSL https://raw.githubusercontent.com/Leisser/trading/main/deploy-to-server.sh | bash
```

### **3. Manual Deployment (Alternative)**
```bash
# Clone the repository
git clone https://github.com/Leisser/trading.git /opt/fluxor
cd /opt/fluxor

# Copy production environment
cp env.production .env

# Update environment variables
sed -i "s/YOUR_SERVER_IP/31.97.103.64/g" .env

# Install Docker (if not installed)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl start docker
systemctl enable docker

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Deploy the application
docker-compose -f docker-compose.prod.yml up -d --build
```

## **DNS Configuration**

### **Required DNS Records**
Configure these A records in your domain provider:

```
Record Type | Name                | Value
-----------|---------------------|------------------
A          | fluxor.pro          | 31.97.103.64
A          | www.fluxor.pro     | 31.97.103.64
A          | api.fluxor.pro     | 31.97.103.64
A          | dashboard.fluxor.pro| 31.97.103.64
A          | db.fluxor.pro      | 31.97.103.64
```

## **SSL Certificate Setup**

### **Install Certbot**
```bash
# Ubuntu/Debian
apt update
apt install certbot python3-certbot-nginx

# CentOS/RHEL
yum install certbot python3-certbot-nginx
```

### **Generate SSL Certificates**
```bash
certbot certonly --nginx -d fluxor.pro -d www.fluxor.pro -d api.fluxor.pro -d dashboard.fluxor.pro -d db.fluxor.pro --non-interactive --agree-tos --email admin@fluxor.pro
```

## **Service Management**

### **View Logs**
```bash
# All services
docker-compose -f /opt/fluxor/docker-compose.prod.yml logs -f

# Specific service
docker-compose -f /opt/fluxor/docker-compose.prod.yml logs -f nginx
docker-compose -f /opt/fluxor/docker-compose.prod.yml logs -f web
```

### **Restart Services**
```bash
cd /opt/fluxor
docker-compose -f docker-compose.prod.yml restart
```

### **Update Application**
```bash
cd /opt/fluxor
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build
```

### **Stop Services**
```bash
cd /opt/fluxor
docker-compose -f docker-compose.prod.yml down
```

## **Monitoring & Maintenance**

### **Health Checks**
```bash
# Check if all containers are running
docker-compose -f /opt/fluxor/docker-compose.prod.yml ps

# Test endpoints
curl -f http://localhost/health/
curl -f http://localhost/api/health/
```

### **Backup Database**
```bash
# Create database backup
docker-compose -f /opt/fluxor/docker-compose.prod.yml exec db pg_dump -U postgres fluxor_prod > /opt/fluxor-backups/backup_$(date +%Y%m%d_%H%M%S).sql
```

### **Disk Space Monitoring**
```bash
# Check disk usage
df -h

# Clean up old Docker images
docker system prune -f
```

## **Security Configuration**

### **Firewall Setup**
```bash
# Allow necessary ports
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

### **SSH Security**
```bash
# Disable root login (recommended)
# Create a new user and use sudo instead
adduser fluxor
usermod -aG sudo fluxor
```

## **Troubleshooting**

### **Common Issues**

1. **Containers not starting**
   ```bash
   docker-compose -f /opt/fluxor/docker-compose.prod.yml logs
   ```

2. **Port conflicts**
   ```bash
   netstat -tulpn | grep :80
   netstat -tulpn | grep :443
   ```

3. **Permission issues**
   ```bash
   chown -R root:root /opt/fluxor
   chmod -R 755 /opt/fluxor
   ```

### **Reset Everything**
```bash
# Stop and remove all containers
docker-compose -f /opt/fluxor/docker-compose.prod.yml down -v

# Remove all images
docker system prune -a -f

# Restart deployment
cd /opt/fluxor
docker-compose -f docker-compose.prod.yml up -d --build
```

## **Access URLs**

After successful deployment:

- **Main App**: http://fluxor.pro
- **API**: http://api.fluxor.pro
- **Dashboard**: http://dashboard.fluxor.pro
- **Database Admin**: http://db.fluxor.pro

## **Support**

If you encounter any issues:

1. Check the logs: `docker-compose logs -f`
2. Verify DNS propagation: `nslookup fluxor.pro`
3. Test connectivity: `curl -I http://fluxor.pro`
4. Check firewall: `ufw status`

## **Performance Optimization**

### **Resource Limits**
Add resource limits to docker-compose.prod.yml:
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

### **Caching**
The nginx configuration includes gzip compression and static file caching for optimal performance.

---

**🎉 Your Fluxor Trading Platform is ready for production!**
