docker --version
docker-compose --version
docker-compose -f docker-compose.prod.yml restart
docker ps -a
docker-compose -f docker-compose.prod.yml logs web
docker-compose -f docker-compose.prod.yml restart
docker-compose -f docker-compose.prod.yml exec db psql -U cmsuser -d cmsdb
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d
docker system prune -a
df -h
# Deployment Guide

This guide covers building images for Django (cmsapp), Nginx, and Postgres, pushing them to AWS ECR, and running production locally with Docker Compose.

## Prerequisites
- Docker and Docker Compose installed
- AWS CLI v2 installed and configured (for ECR pushes)
- An AWS account ID and permissions to create ECR repositories

## 1) Configure environment

```bash
cp .env.example .env
```

Key variables in .env (see [.env.example](.env.example)):
- Application: `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DJANGO_SUPERUSER_*`
- AWS/ECR: `AWS_REGION`, `AWS_ACCOUNT_ID`, `ECR_REPO_WEB`, `ECR_REPO_NGINX`, `ECR_REPO_POSTGRES`, `IMAGE_TAG`, `AWS_PROFILE` (optional)

## 2) Build and push images to ECR

Script: [build-ecr-images.sh](build-ecr-images.sh)

```bash
cd cmsapp
chmod +x build-ecr-images.sh
set -a && source .env && set +a
./build-ecr-images.sh
```

What it does:
- Ensures three ECR repositories exist: web, nginx, postgres
- Builds images using:
  - [Dockerfile](Dockerfile) (web)
  - [Dockerfile.nginx](Dockerfile.nginx) (nginx)
  - [Dockerfile.postgres](Dockerfile.postgres) (postgres)
- Tags all images as `$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/<repo>:$IMAGE_TAG` and pushes to ECR

Required env: `AWS_REGION`, `AWS_ACCOUNT_ID`, `ECR_REPO_WEB`, `ECR_REPO_NGINX`, `ECR_REPO_POSTGRES`
Optional: `IMAGE_TAG` (default `prod`), `AWS_PROFILE`

## 3) Run production locally with Compose

Option A: Use the helper script [build-prod.sh](build-prod.sh) (builds images locally and starts services):

```bash
chmod +x build-prod.sh
./build-prod.sh
```

Option B: Manual commands:

```bash
docker pull python:3.12-slim postgres:16-alpine nginx:alpine
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

Services (see [docker-compose.prod.yml](docker-compose.prod.yml)):
- `db`: Postgres 16, persists to `postgres_data`
- `web`: Django app (gunicorn), runs migrations, collectstatic, creates superuser
- `nginx`: reverse proxy serving static/media

Useful commands:

```bash
# Logs
docker-compose -f docker-compose.prod.yml logs -f

# Migrations / collectstatic
docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Stop
docker-compose -f docker-compose.prod.yml down
```

## 4) SSL and Nginx
The default [nginx.conf](nginx.conf) listens on 80/443. For Let’s Encrypt, obtain certificates and mount them (e.g., via host volumes or image customization) then update nginx.conf accordingly.

## 5) Backups (example)

```bash
cat > /opt/cmsapp/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/cmsapp/backups"
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker-compose -f /opt/cmsapp/docker-compose.prod.yml exec -T db pg_dump -U cmsuser cmsdb | gzip > "$BACKUP_DIR/cmsdb_$TIMESTAMP.sql.gz"
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete
EOF
chmod +x /opt/cmsapp/backup.sh
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/cmsapp/backup.sh") | crontab -
```

## 6) Troubleshooting
- Check status: `docker ps -a`
- Logs: `docker-compose -f docker-compose.prod.yml logs -f web db nginx`
- Recreate cleanly: `docker-compose -f docker-compose.prod.yml down -v && docker-compose -f docker-compose.prod.yml up -d`

## Security checklist
- SECRET_KEY is unique and strong
- DEBUG=False
- ALLOWED_HOSTS is set
- SSL/HTTPS enabled at the edge (nginx / load balancer)
- Database password is strong
- Backups scheduled and tested
- Regular image rebuilds and updates applied
docker-compose -f docker-compose.prod.yml logs -f db
