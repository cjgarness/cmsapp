#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${1:-docker-compose.dev.yml}"
SERVICE_NAME="${2:-web}"

echo "[rebuild-web] Using compose file: ${COMPOSE_FILE}"
echo "[rebuild-web] Target service: ${SERVICE_NAME}"

echo "[rebuild-web] Stopping service..."
docker compose -f "${COMPOSE_FILE}" stop "${SERVICE_NAME}"

echo "[rebuild-web] Removing container..."
docker compose -f "${COMPOSE_FILE}" rm -f "${SERVICE_NAME}"

echo "[rebuild-web] Building image..."
docker compose -f "${COMPOSE_FILE}" build "${SERVICE_NAME}"

echo "[rebuild-web] Starting service..."
docker compose -f "${COMPOSE_FILE}" up -d "${SERVICE_NAME}"

echo "[rebuild-web] Done."
