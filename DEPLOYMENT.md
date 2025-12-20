# Deployment Guide

## Prerequisites

- Ubuntu 20.04+ server
- Docker and Docker Compose installed
- Domain name (for production)
- SSL certificate (for HTTPS)

## Step 1: Server Setup

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

## Step 2: Clone Repository

```bash
cd /opt
sudo git clone https://github.com/your-repo/cmsapp.git
cd cmsapp
sudo chown -R $USER:$USER .
```

## Step 3: Configure Environment

```bash
cp .env.example .env
nano .env
```

### Production .env Settings

```env
DEBUG=False
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_PASSWORD=StrongPassword123!
DATABASE_HOST=db
DATABASE_NAME=cmsdb
DATABASE_USER=cmsuser
DJANGO_SETTINGS_MODULE=cmsapp.settings
```

## Step 4: Deploy

```bash
chmod +x build-prod.sh
./build-prod.sh
```

## Step 5: SSL Configuration

### Using Let's Encrypt

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

### Update nginx.conf

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # ... rest of nginx config
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## Step 6: Create Superuser

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

## Step 7: Monitoring & Maintenance

### View Logs

```bash
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f db
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Database Backup (Daily)

```bash
# Create backup script
cat > /opt/cmsapp/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/cmsapp/backups"
mkdir -p $BACKUP_DIR
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U cmsuser cmsdb | gzip > $BACKUP_DIR/cmsdb_$TIMESTAMP.sql.gz
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
EOF

# Make executable and add to cron
chmod +x /opt/cmsapp/backup.sh
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/cmsapp/backup.sh") | crontab -
```

### Update Images (Monthly)

```bash
docker pull python:3.12-slim
docker pull postgres:16-alpine
docker pull nginx:alpine
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml restart
```

## Troubleshooting

### Service Won't Start

```bash
# Check Docker status
docker ps -a

# View detailed logs
docker-compose -f docker-compose.prod.yml logs web

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

### Database Issues

```bash
# Check database container
docker-compose -f docker-compose.prod.yml exec db psql -U cmsuser -d cmsdb

# Recreate database
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d
```

### Out of Disk Space

```bash
# Remove unused containers and images
docker system prune -a

# Check disk usage
df -h
```

## Performance Tuning

### Nginx Caching

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m use_temp_path=off;

location / {
    proxy_cache api_cache;
    proxy_cache_valid 200 1h;
    # ... other config
}
```

### Database Connection Pool

```python
# In settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Connection pooling
        # ... other settings
    }
}
```

## Security Checklist

- [ ] SECRET_KEY is unique and strong
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS configured correctly
- [ ] SSL/HTTPS enabled
- [ ] Database password is strong
- [ ] Regular backups configured
- [ ] Log monitoring in place
- [ ] Firewall rules configured
- [ ] Regular security updates applied
- [ ] Automated tests passing

---

For more information, see [README.md](README.md)
