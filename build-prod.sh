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
