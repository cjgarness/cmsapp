#!/bin/bash
# PostgreSQL database backup script for CMS application

set -e

# Configuration
ENVIRONMENT=${1:-dev}
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Set compose file based on environment
if [ "$ENVIRONMENT" = "dev" ]; then
    COMPOSE_FILE="docker-compose.dev.yml"
    CONTAINER_NAME="cmsapp_db_dev"
    DB_NAME="${DATABASE_NAME:-cmsdb}"
    DB_USER="${DATABASE_USER:-cmsuser}"
elif [ "$ENVIRONMENT" = "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    CONTAINER_NAME="cmsapp_db_prod"
    DB_NAME="${DATABASE_NAME:-cmsdb}"
    DB_USER="${DATABASE_USER:-cmsuser}"
else
    echo "Usage: ./backup-db.sh [dev|prod] [custom_name]"
    echo "  Example: ./backup-db.sh dev"
    echo "  Example: ./backup-db.sh prod pre-migration"
    exit 1
fi

# Custom backup name (optional)
CUSTOM_NAME="${2}"
if [ -n "$CUSTOM_NAME" ]; then
    BACKUP_FILENAME="${CUSTOM_NAME}_${TIMESTAMP}.sql"
else
    BACKUP_FILENAME="cmsdb_backup_${TIMESTAMP}.sql"
fi

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Full path to backup file
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILENAME}"

echo "========================================"
echo "Database Backup Script"
echo "========================================"
echo "Environment: $ENVIRONMENT"
echo "Database: $DB_NAME"
echo "Container: $CONTAINER_NAME"
echo "Backup file: $BACKUP_PATH"
echo "========================================"

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Error: Container $CONTAINER_NAME is not running"
    echo "Start the application first with: ./build-${ENVIRONMENT}.sh"
    exit 1
fi

# Perform the backup
echo "Starting backup..."
docker exec -t "$CONTAINER_NAME" pg_dump -U "$DB_USER" -d "$DB_NAME" --clean --if-exists > "$BACKUP_PATH"

# Check if backup was successful
if [ $? -eq 0 ] && [ -s "$BACKUP_PATH" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_PATH" | cut -f1)
    echo "✓ Backup completed successfully!"
    echo "  File: $BACKUP_PATH"
    echo "  Size: $BACKUP_SIZE"
    
    # Compress the backup (optional)
    echo "Compressing backup..."
    gzip "$BACKUP_PATH"
    COMPRESSED_PATH="${BACKUP_PATH}.gz"
    COMPRESSED_SIZE=$(du -h "$COMPRESSED_PATH" | cut -f1)
    echo "✓ Backup compressed: $COMPRESSED_PATH"
    echo "  Compressed size: $COMPRESSED_SIZE"
    
    # Keep only the last 10 backups
    echo "Cleaning up old backups (keeping last 10)..."
    cd "$BACKUP_DIR"
    ls -t cmsdb_backup_*.sql.gz 2>/dev/null | tail -n +11 | xargs -r rm --
    cd - > /dev/null
    
    BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/cmsdb_backup_*.sql.gz 2>/dev/null | wc -l)
    echo "✓ Total backups in storage: $BACKUP_COUNT"
    
else
    echo "✗ Backup failed!"
    rm -f "$BACKUP_PATH"
    exit 1
fi

echo "========================================"
echo "Backup process completed!"
echo "========================================"
