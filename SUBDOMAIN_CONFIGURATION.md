# 🌐 Fluxor Trading Platform - Subdomain Configuration

## **Fluxor Trading Platform - Subdomain Structure**

### **Primary Domains (Required)**
1. **`fluxor.pro`** - Main trading application (Next.js web)
2. **`api.fluxor.pro`** - Backend API (Django REST API)
3. **`dashboard.fluxor.pro`** - Admin dashboard (Vue.js dashboard)
4. **`db.fluxor.pro`** - Database management (pgAdmin)

## **DNS Configuration**

### **A Records to Create:**
```
fluxor.pro          A    YOUR_SERVER_IP
www.fluxor.pro      A    YOUR_SERVER_IP
api.fluxor.pro      A    YOUR_SERVER_IP
dashboard.fluxor.pro A   YOUR_SERVER_IP
db.fluxor.pro       A    YOUR_SERVER_IP
```

### **CNAME Records (Alternative):**
```
api.fluxor.pro      CNAME fluxor.pro
dashboard.fluxor.pro CNAME fluxor.pro
db.fluxor.pro       CNAME fluxor.pro
```

## **Service Mapping**

| Subdomain | Service | Port | Purpose | Access Level |
|-----------|---------|------|---------|--------------|
| `fluxor.pro` | Web (Next.js) | 5173 | Main trading app | Public |
| `api.fluxor.pro` | Backend (Django) | 8000 | REST API | Public (with auth) |
| `dashboard.fluxor.pro` | Dashboard (Vue.js) | 3001 | Admin dashboard | Superuser only |
| `db.fluxor.pro` | pgAdmin | 5050 | Database management | Admin only |

## **Security Configuration**

### **Access Control:**
- **`fluxor.pro`**: Public access
- **`api.fluxor.pro`**: Public with authentication
- **`dashboard.fluxor.pro`**: Superuser authentication required
- **`db.fluxor.pro`**: Basic auth + database credentials

### **SSL/TLS Configuration:**
All subdomains should use HTTPS with Let's Encrypt certificates:
```bash
# Generate certificates for all subdomains
certbot certonly --nginx -d fluxor.pro -d www.fluxor.pro -d api.fluxor.pro -d dashboard.fluxor.pro -d db.fluxor.pro
```

## **Environment Variables**

### **Web Configuration:**
```bash
# web/.env.production
NEXT_PUBLIC_API_URL=https://api.fluxor.pro
NEXT_PUBLIC_WS_URL=wss://api.fluxor.pro
NEXT_PUBLIC_DASHBOARD_URL=https://dashboard.fluxor.pro
```

### **Backend Configuration:**
```bash
# fluxor_api/.env.production
ALLOWED_HOSTS=fluxor.pro,www.fluxor.pro,api.fluxor.pro,dashboard.fluxor.pro,admin.fluxor.pro,docs.fluxor.pro,status.fluxor.pro,monitoring.fluxor.pro
CORS_ALLOWED_ORIGINS=https://fluxor.pro,https://dashboard.fluxor.pro
```

## **Nginx Configuration**

The nginx configuration has been updated to handle all subdomains with:
- Proper routing to respective services
- Security headers
- Rate limiting
- CORS configuration
- SSL termination

## **Deployment Steps**

1. **Configure DNS**: Add A records for all subdomains
2. **SSL Certificates**: Generate Let's Encrypt certificates
3. **Environment Variables**: Update production environment files
4. **Deploy Services**: Run `docker-compose -f docker-compose.prod.yml up -d`
5. **Verify Access**: Test all subdomains

## **Monitoring & Maintenance**

### **Health Checks:**
- `https://status.fluxor.pro` - System status
- `https://api.fluxor.pro/health/` - API health check
- `https://fluxor.pro/health/` - Frontend health check

### **Logs:**
```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f nginx
docker-compose logs -f api
docker-compose logs -f web
docker-compose logs -f dashboard
```

## **Backup Strategy**

### **Database Backups:**
```bash
# Backup PostgreSQL
docker-compose exec db pg_dump -U postgres fluxor_api > backup_$(date +%Y%m%d_%H%M%S).sql
```

### **Volume Backups:**
```bash
# Backup all volumes
docker run --rm -v fluxor_postgres_data:/data -v $(pwd)/backups:/backup alpine tar czf /backup/postgres_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
```

## **Scaling Considerations**

### **Load Balancer Setup:**
For high traffic, consider using a load balancer (HAProxy, Nginx Plus, or cloud load balancer) in front of the nginx reverse proxy.

### **CDN Integration:**
Consider using a CDN (Cloudflare, AWS CloudFront) for static assets and global distribution.

### **Database Scaling:**
- Read replicas for read-heavy operations
- Connection pooling (PgBouncer)
- Database clustering for high availability

## **Security Best Practices**

1. **Firewall Configuration**: Only allow necessary ports (80, 443, 22)
2. **Regular Updates**: Keep all containers and dependencies updated
3. **Monitoring**: Set up alerts for unusual activity
4. **Backup Encryption**: Encrypt database backups
5. **Access Logs**: Monitor and analyze access patterns
6. **Rate Limiting**: Implement rate limiting for all endpoints
7. **DDoS Protection**: Use DDoS protection services

## **Cost Optimization**

### **Resource Allocation:**
- **Development**: 2 CPU, 4GB RAM
- **Production**: 4 CPU, 8GB RAM minimum
- **High Traffic**: 8 CPU, 16GB RAM+

### **Storage Requirements:**
- **Database**: 50GB minimum
- **Logs**: 10GB minimum
- **Backups**: 100GB minimum
- **Static Files**: 5GB minimum

This configuration provides a robust, scalable, and secure setup for the Fluxor Trading Platform with proper separation of concerns and access controls.
