#!/bin/bash
# Database migration helper script

ENVIRONMENT=${1:-dev}

if [ "$ENVIRONMENT" = "dev" ]; then
    COMPOSE_FILE="docker-compose.dev.yml"
    COMPOSE_CMD="docker-compose -f $COMPOSE_FILE"
elif [ "$ENVIRONMENT" = "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    COMPOSE_CMD="docker-compose -f $COMPOSE_FILE"
else
    echo "Usage: ./migrate.sh [dev|prod]"
    exit 1
fi

case "$2" in
    make)
        echo "Creating migrations..."
        $COMPOSE_CMD exec web python manage.py makemigrations core media pages templates
        ;;
    migrate)
        echo "Applying migrations..."
        $COMPOSE_CMD exec web python manage.py migrate
        ;;
    show)
        echo "Migration status..."
        $COMPOSE_CMD exec web python manage.py showmigrations
        ;;
    *)
        echo "Usage: ./migrate.sh [dev|prod] [make|migrate|show]"
        exit 1
        ;;
esac
