#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${1:-docker-compose.prod.yml}"
SERVICE_NAME="${2:-web}"

echo "[rebuild-web-prod] Using compose file: ${COMPOSE_FILE}"
echo "[rebuild-web-prod] Target service: ${SERVICE_NAME}"

echo "[rebuild-web-prod] Stopping service..."
docker compose -f "${COMPOSE_FILE}" stop "${SERVICE_NAME}"

echo "[rebuild-web-prod] Removing container..."
docker compose -f "${COMPOSE_FILE}" rm -f "${SERVICE_NAME}"

echo "[rebuild-web-prod] Building image..."
docker compose -f "${COMPOSE_FILE}" build "${SERVICE_NAME}"

echo "[rebuild-web-prod] Starting service..."
docker compose -f "${COMPOSE_FILE}" up -d "${SERVICE_NAME}"

echo "[rebuild-web-prod] Done."
