#!/bin/bash
# Helper script to manage the CMS application

set -e

ENVIRONMENT=${1:-dev}
COMMAND=${2}

if [ "$ENVIRONMENT" != "dev" ] && [ "$ENVIRONMENT" != "prod" ]; then
    echo "Usage: ./manage.sh [dev|prod] [command] [args...]"
    echo ""
    echo "Commands:"
    echo "  createsuperuser - Create a Django superuser"
    echo "  shell          - Open Django shell"
    echo "  dbshell        - Open database shell"
    echo "  clearcache     - Clear all caches"
    echo "  staticfiles    - Collect static files"
    echo "  help           - Show Django help"
    exit 1
fi

COMPOSE_FILE="docker-compose.${ENVIRONMENT}.yml"
COMPOSE_CMD="docker-compose -f $COMPOSE_FILE"

case "$COMMAND" in
    createsuperuser)
        $COMPOSE_CMD exec web python manage.py createsuperuser
        ;;
    shell)
        $COMPOSE_CMD exec web python manage.py shell
        ;;
    dbshell)
        $COMPOSE_CMD exec db psql -U cmsuser -d cmsdb
        ;;
    clearcache)
        echo "Clearing cache..."
        $COMPOSE_CMD exec web python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('Cache cleared')"
        ;;
    staticfiles)
        echo "Collecting static files..."
        $COMPOSE_CMD exec web python manage.py collectstatic --noinput
        ;;
    help)
        $COMPOSE_CMD exec web python manage.py help
        ;;
    *)
        echo "Running: python manage.py $COMMAND"
        $COMPOSE_CMD exec web python manage.py "$COMMAND"
        ;;
esac
