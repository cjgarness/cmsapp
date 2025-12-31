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

## 5) Database Backups

The application includes dedicated backup scripts for both development and production environments.

### Production Backup Script

The production backup script ([backup-db-prod.sh](backup-db-prod.sh)) provides automated retention policies and organized storage:

```bash
# Standard backup
./backup-db-prod.sh

# Named backup (for special occasions like pre-migration)
./backup-db-prod.sh pre-migration
```

**Features:**
- **Automatic retention policy**: Daily (7 days), Weekly (4 weeks), Monthly (6 months)
- **Organized storage**: Separate directories for daily/weekly/monthly backups
- **Compression**: Automatic gzip compression
- **Verification**: Checks container status and backup integrity
- **Tracking**: Shows backup counts and total storage used

**Backup Structure:**
```
backups/prod/
├── daily/         # Last 7 days
├── weekly/        # Last 4 weeks (Sundays)
├── monthly/       # Last 6 months (1st of month)
└── prod_cmsdb_*.sql.gz  # Individual timestamped backups
```

### Automated Daily Backups

Set up a cron job to run backups automatically:

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 2 AM
0 2 * * * cd /path/to/cmsapp && ./backup-db-prod.sh >> /var/log/cmsapp-backup.log 2>&1
```

### Development Backup Script

For development environments, use the general backup script:

```bash
# Development backup
./backup-db.sh dev

# Named development backup
./backup-db.sh dev before-major-changes
```

### Manual Backup

For one-off backups without using the scripts:

```bash
# Create backup directory
mkdir -p backups/manual

# Create backup
docker exec -t cmsapp_db_prod pg_dump -U cmsuser -d cmsdb --clean --if-exists | gzip > backups/manual/manual_$(date +%Y%m%d_%H%M%S).sql.gz
```

### Restore from Backup

To restore a database from a backup:

```bash
# Stop the web service
docker-compose -f docker-compose.prod.yml stop web

# Restore the backup
gunzip -c backups/prod/prod_cmsdb_TIMESTAMP.sql.gz | docker exec -i cmsapp_db_prod psql -U cmsuser -d cmsdb

# Restart the web service
docker-compose -f docker-compose.prod.yml start web
```

### Backup Best Practices

1. **Test restores regularly** - Verify backups can be restored successfully
2. **Store off-site** - Copy backups to remote storage (S3, rsync to remote server, etc.)
3. **Monitor backup size** - Check disk space usage periodically
4. **Verify integrity** - Ensure backup files are not corrupted
5. **Document procedures** - Keep restore instructions accessible

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
