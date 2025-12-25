#!/bin/bash
# Renew Let's Encrypt certificates inside the nginx container and reload nginx

set -e

if ! docker compose version &> /dev/null; then
    echo "ERROR: Docker Compose plugin not found."
    exit 1
fi

COMPOSE_FILE=${COMPOSE_FILE:-docker-compose.prod.yml}

echo "Running certbot renew..."
docker compose -f "$COMPOSE_FILE" exec -T nginx certbot renew

echo "Reloading nginx..."
docker compose -f "$COMPOSE_FILE" exec -T nginx nginx -s reload

echo "Done."
