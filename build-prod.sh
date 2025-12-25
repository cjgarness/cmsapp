#!/bin/bash
# Build and deploy the Django CMS application in production mode

set -e

echo "======================================"
echo "Django CMS - Production Build Script"
echo "======================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please create .env file with production settings."
    exit 1
fi

# Validate required environment variables
required_vars=("SECRET_KEY" "DATABASE_USER" "DATABASE_PASSWORD" "ALLOWED_HOSTS")
for var in "${required_vars[@]}"; do
    if ! grep -q "^$var=" .env; then
        echo "ERROR: $var not found in .env file"
        exit 1
    fi
done

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not found. Please install Docker."
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "ERROR: Docker Compose plugin not found. Please install the Docker Compose plugin for Docker." 
    exit 1
fi

echo ""
echo "Pulling latest base images..."
docker pull python:3.12-slim
docker pull postgres:16-alpine
docker pull nginx:alpine

echo ""
echo "Building production Docker images..."
docker compose -f docker-compose.prod.yml build --no-cache

echo ""
echo "Starting production services..."
docker compose -f docker-compose.prod.yml up -d

echo ""
echo "Waiting for database to be ready..."
sleep 15

echo ""
echo "Running database migrations..."
docker compose -f docker-compose.prod.yml exec -T web python manage.py migrate

echo ""
echo "Collecting static files..."
docker compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput
echo ""
echo "Attempting to obtain TLS certificates with Certbot..."
# Load CERTBOT_EMAIL from .env if present
CERTBOT_EMAIL_VAR=$(grep -E '^CERTBOT_EMAIL=' .env | cut -d'=' -f2- || true)
if [ -z "$CERTBOT_EMAIL_VAR" ]; then
    echo "WARNING: CERTBOT_EMAIL not set in .env. Skipping certificate issuance."
    echo "To enable TLS, add CERTBOT_EMAIL to .env and re-run:"
    echo "  docker compose -f docker-compose.prod.yml exec nginx certbot certonly --webroot -w /var/www/certbot -d rvscope.com -d www.rvscope.com -d altuspath.com -d www.altuspath.com --agree-tos -m you@example.com --non-interactive --rsa-key-size 4096"
else
    docker compose -f docker-compose.prod.yml exec -T nginx certbot certonly --webroot -w /var/www/certbot \
        -d rvscope.com -d www.rvscope.com -d altuspath.com -d www.altuspath.com \
        --agree-tos -m "$CERTBOT_EMAIL_VAR" --non-interactive --rsa-key-size 4096 || true
    echo "Reloading Nginx to apply certificates..."
    docker compose -f docker-compose.prod.yml exec -T nginx nginx -s reload || true
fi

echo ""
echo "======================================"
echo "Production deployment successful!"
echo "======================================"
echo ""
echo "Access the application at: http://localhost"
echo "Access admin panel at: http://localhost/admin"
echo ""
echo "Useful commands:"
echo "  - View logs: docker compose -f docker-compose.prod.yml logs -f"
echo "  - Create superuser: docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"
echo "  - Stop services: docker compose -f docker-compose.prod.yml down"
echo "  - Restart services: docker compose -f docker-compose.prod.yml restart"
echo ""
echo "Certbot tips:"
echo "  - Issue/renew: docker compose -f docker-compose.prod.yml exec nginx certbot renew && docker compose -f docker-compose.prod.yml exec nginx nginx -s reload"
echo "  - First issue (if skipped): docker compose -f docker-compose.prod.yml exec nginx certbot certonly --webroot -w /var/www/certbot -d rvscope.com -d www.rvscope.com -d altuspath.com -d www.altuspath.com --agree-tos -m \$CERTBOT_EMAIL --non-interactive"
echo ""
echo ""
