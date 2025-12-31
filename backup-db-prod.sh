#!/bin/bash
# Production PostgreSQL database backup script for CMS application
# This script creates timestamped backups with compression and retention policies

set -e

# Configuration
BACKUP_DIR="./backups/prod"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DATE_ONLY=$(date +"%Y%m%d")
CONTAINER_NAME="cmsapp_db_prod"
DB_NAME="${DATABASE_NAME:-cmsdb}"
DB_USER="${DATABASE_USER:-cmsuser}"

# Retention settings
DAILY_RETENTION=7      # Keep daily backups for 7 days
WEEKLY_RETENTION=4     # Keep weekly backups for 4 weeks
MONTHLY_RETENTION=6    # Keep monthly backups for 6 months

# Custom backup name (optional)
CUSTOM_NAME="${1}"
if [ -n "$CUSTOM_NAME" ]; then
    BACKUP_FILENAME="prod_${CUSTOM_NAME}_${TIMESTAMP}.sql"
else
    BACKUP_FILENAME="prod_cmsdb_${TIMESTAMP}.sql"
fi

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"
mkdir -p "$BACKUP_DIR/daily"
mkdir -p "$BACKUP_DIR/weekly"
mkdir -p "$BACKUP_DIR/monthly"

# Full path to backup file
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILENAME}"

echo "========================================"
echo "Production Database Backup"
echo "========================================"
echo "Database: $DB_NAME"
echo "Container: $CONTAINER_NAME"
echo "Timestamp: $TIMESTAMP"
echo "========================================"

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "✗ Error: Container $CONTAINER_NAME is not running"
    echo "Start the application first with: ./build-prod.sh"
    exit 1
fi

# Perform the backup
echo "Creating backup..."
if docker exec -t "$CONTAINER_NAME" pg_dump -U "$DB_USER" -d "$DB_NAME" --clean --if-exists > "$BACKUP_PATH" 2>/dev/null; then
    echo "✓ Backup created successfully"
else
    echo "✗ Backup failed!"
    rm -f "$BACKUP_PATH"
    exit 1
fi

# Verify backup file exists and has content
if [ ! -s "$BACKUP_PATH" ]; then
    echo "✗ Backup file is empty or doesn't exist"
    rm -f "$BACKUP_PATH"
    exit 1
fi

BACKUP_SIZE=$(du -h "$BACKUP_PATH" | cut -f1)
echo "  File: $BACKUP_FILENAME"
echo "  Size: $BACKUP_SIZE"

# Compress the backup
echo "Compressing backup..."
gzip "$BACKUP_PATH"
COMPRESSED_PATH="${BACKUP_PATH}.gz"
COMPRESSED_SIZE=$(du -h "$COMPRESSED_PATH" | cut -f1)
echo "✓ Compressed: $COMPRESSED_SIZE"

# Copy to appropriate retention directory
DAY_OF_WEEK=$(date +%u)  # 1=Monday, 7=Sunday
DAY_OF_MONTH=$(date +%d)

# Monthly backup (keep on 1st of month)
if [ "$DAY_OF_MONTH" = "01" ]; then
    MONTHLY_BACKUP="${BACKUP_DIR}/monthly/monthly_${DATE_ONLY}.sql.gz"
    cp "$COMPRESSED_PATH" "$MONTHLY_BACKUP"
    echo "✓ Monthly backup saved"
fi

# Weekly backup (keep on Sundays)
if [ "$DAY_OF_WEEK" = "7" ]; then
    WEEKLY_BACKUP="${BACKUP_DIR}/weekly/weekly_${DATE_ONLY}.sql.gz"
    cp "$COMPRESSED_PATH" "$WEEKLY_BACKUP"
    echo "✓ Weekly backup saved"
fi

# Daily backup (always)
DAILY_BACKUP="${BACKUP_DIR}/daily/daily_${DATE_ONLY}.sql.gz"
cp "$COMPRESSED_PATH" "$DAILY_BACKUP"
echo "✓ Daily backup saved"

# Cleanup old backups based on retention policies
echo ""
echo "Applying retention policies..."

# Remove daily backups older than DAILY_RETENTION days
find "$BACKUP_DIR/daily" -name "daily_*.sql.gz" -mtime +$DAILY_RETENTION -delete 2>/dev/null
DAILY_COUNT=$(ls -1 "$BACKUP_DIR/daily/"daily_*.sql.gz 2>/dev/null | wc -l)
echo "  Daily backups: $DAILY_COUNT (retention: ${DAILY_RETENTION} days)"

# Remove weekly backups older than WEEKLY_RETENTION weeks
find "$BACKUP_DIR/weekly" -name "weekly_*.sql.gz" -mtime +$((WEEKLY_RETENTION * 7)) -delete 2>/dev/null
WEEKLY_COUNT=$(ls -1 "$BACKUP_DIR/weekly/"weekly_*.sql.gz 2>/dev/null | wc -l)
echo "  Weekly backups: $WEEKLY_COUNT (retention: ${WEEKLY_RETENTION} weeks)"

# Remove monthly backups older than MONTHLY_RETENTION months
find "$BACKUP_DIR/monthly" -name "monthly_*.sql.gz" -mtime +$((MONTHLY_RETENTION * 30)) -delete 2>/dev/null
MONTHLY_COUNT=$(ls -1 "$BACKUP_DIR/monthly/"monthly_*.sql.gz 2>/dev/null | wc -l)
echo "  Monthly backups: $MONTHLY_COUNT (retention: ${MONTHLY_RETENTION} months)"

# Calculate total backup size
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo "  Total backup storage: $TOTAL_SIZE"

# Optional: Send notification (uncomment and configure as needed)
# if command -v mail &> /dev/null; then
#     echo "Database backup completed successfully on $(date)" | \
#     mail -s "CMS Production Database Backup - Success" admin@example.com
# fi

echo ""
echo "========================================"
echo "✓ Backup completed successfully!"
echo "========================================"
echo "Latest backup: $BACKUP_FILENAME.gz"
echo "Location: $BACKUP_DIR"
echo ""
echo "Retention summary:"
echo "  - Daily: Last $DAILY_RETENTION days ($DAILY_COUNT backups)"
echo "  - Weekly: Last $WEEKLY_RETENTION weeks ($WEEKLY_COUNT backups)"  
echo "  - Monthly: Last $MONTHLY_RETENTION months ($MONTHLY_COUNT backups)"
echo "========================================"

exit 0
