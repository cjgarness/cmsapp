#!/bin/bash
# Build and deploy the Django CMS application in production mode

set -e

# Parse command line arguments
SKIP_SSL=false
for arg in "$@"; do
    case $arg in
        --skip-ssl)
            SKIP_SSL=true
            shift
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Usage: $0 [--skip-ssl]"
            echo "  --skip-ssl: Skip SSL certificate generation (useful for updates)"
            exit 1
            ;;
    esac
done

echo "======================================"
echo "Django CMS - Production Build Script"
echo "======================================"
if [ "$SKIP_SSL" = true ]; then
    echo "Mode: Skipping SSL certificate generation"
fi
echo ""

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
echo "Fixing permissions on certbot directory..."
if [ -d "./certbot" ]; then
    sudo chown -R $USER:$USER ./certbot 2>/dev/null || true
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

if [ "$SKIP_SSL" = true ]; then
    echo ""
    echo "Skipping SSL certificate generation (--skip-ssl flag set)"
else
    echo ""
    echo "Attempting to obtain TLS certificates with Certbot..."
    # Load CERTBOT_EMAIL and TEST_CERTBOT from .env if present
    CERTBOT_EMAIL_VAR=$(grep -E '^CERTBOT_EMAIL=' .env | cut -d'=' -f2- || true)
    TEST_CERTBOT_VAR=$(grep -E '^TEST_CERTBOT=' .env | cut -d'=' -f2- || true)

    if [ -z "$CERTBOT_EMAIL_VAR" ]; then
        echo "WARNING: CERTBOT_EMAIL not set in .env. Skipping certificate issuance."
        echo "Using self-signed certificates instead."
    else
        # Determine if we're in test mode
        TEST_FLAG=""
        if [ "$TEST_CERTBOT_VAR" == "true" ]; then
            TEST_FLAG="--dry-run"
            echo "TEST_CERTBOT=true: Running certbot in DRY-RUN mode (no actual certificates will be issued)"
        fi
        
        # Attempt to obtain certificates
        docker compose -f docker-compose.prod.yml exec -T nginx certbot certonly --webroot -w /var/www/certbot \
            -d rvscope.com -d www.rvscope.com -d altuspath.com -d www.altuspath.com \
            --agree-tos -m "$CERTBOT_EMAIL_VAR" --non-interactive --rsa-key-size 4096 $TEST_FLAG || true
        
        # Check if certificates were successfully obtained (check inside container)
        if docker compose -f docker-compose.prod.yml exec -T nginx test -f /etc/letsencrypt/live/rvscope.com/fullchain.pem 2>/dev/null; then
            echo "✓ Let's Encrypt certificates obtained successfully"
            
            # Verify it's not a self-signed certificate
            CERT_ISSUER=$(docker compose -f docker-compose.prod.yml exec -T nginx openssl x509 -in /etc/letsencrypt/live/rvscope.com/fullchain.pem -noout -issuer 2>/dev/null || true)
            
            if echo "$CERT_ISSUER" | grep -q "Let's Encrypt"; then
                echo "✓ Certificate verified: Issued by Let's Encrypt"
                
                # Remove the archive directory to clean up old self-signed certs
                echo "Cleaning up old self-signed certificate files..."
                docker compose -f docker-compose.prod.yml exec -T nginx sh -c 'rm -rf /etc/letsencrypt/archive/rvscope.com/cert*.pem && rm -rf /etc/letsencrypt/archive/rvscope.com/privkey*.pem 2>/dev/null || true' || true
            fi
            
            if [ "$TEST_CERTBOT_VAR" != "true" ]; then
                echo "Reloading Nginx to apply certificates..."
                docker compose -f docker-compose.prod.yml exec -T nginx nginx -s reload || true
            else
                echo "Skipping Nginx reload (dry-run mode)"
            fi
        else
            echo "⚠ Let's Encrypt certificates not available. Nginx will use self-signed certificates."
            echo "Certbot details:"
            docker compose -f docker-compose.prod.yml exec -T nginx certbot certificates || true
        fi
    fi
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
echo "Build script options:"
echo "  - Skip SSL generation: ./build-prod.sh --skip-ssl"
echo ""
echo "Certbot tips:"
echo "  - Issue/renew: docker compose -f docker-compose.prod.yml exec nginx certbot renew && docker compose -f docker-compose.prod.yml exec nginx nginx -s reload"
echo "  - First issue (if skipped): docker compose -f docker-compose.prod.yml exec nginx certbot certonly --webroot -w /var/www/certbot -d rvscope.com -d www.rvscope.com -d altuspath.com -d www.altuspath.com --agree-tos -m \$CERTBOT_EMAIL --non-interactive"
echo ""
echo ""
