#!/bin/sh
set -e
# Start crond in background (busybox crond daemonizes by default)
crond || echo "[cron] Failed to start crond"
