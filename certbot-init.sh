#!/bin/sh
set -e

# Obtain Let's Encrypt certificates before nginx starts, using standalone mode.
# Requires CERTBOT_EMAIL and CERTBOT_DOMAINS (comma-separated).
# If TEST_CERTBOT=true, uses --staging.

EMAIL="${CERTBOT_EMAIL:-}"
DOMAINS_RAW="${CERTBOT_DOMAINS:-rvscope.com,www.rvscope.com,altuspath.com,www.altuspath.com}"
TEST_FLAG=""

if [ "${TEST_CERTBOT}" = "true" ] || [ "${TEST_CERTBOT}" = "1" ]; then
  TEST_FLAG="--staging"
fi

if [ -z "$EMAIL" ]; then
  echo "[certbot-init] CERTBOT_EMAIL is not set; skipping certificate request."
  exit 0
fi

# Build domain args: filter entries that look like real hostnames (contain a dot and are not pure IPs)
DOMAIN_ARGS=""
PRIMARY_DOMAIN=""
IFS=','
for d in $DOMAINS_RAW; do
  d_trim=$(echo "$d" | tr -d ' ')
  # Skip empty, localhost, and any pure numeric/IP tokens
  if [ -z "$d_trim" ] || [ "$d_trim" = "localhost" ]; then
    continue
  fi
  case "$d_trim" in
    *.*)
      if echo "$d_trim" | grep -Eq '^[0-9.]+$'; then
        # Pure IP address; skip
        continue
      fi
      if [ -z "$PRIMARY_DOMAIN" ]; then
        PRIMARY_DOMAIN="$d_trim"
      fi
      DOMAIN_ARGS="$DOMAIN_ARGS -d $d_trim"
      ;;
    *)
      # No dot; probably not a valid FQDN
      ;;
  esac
done
unset IFS

if [ -z "$DOMAIN_ARGS" ]; then
  echo "[certbot-init] No valid domains to request certificates for; skipping."
  exit 0
fi

LIVE_DIR="/etc/letsencrypt/live/$PRIMARY_DOMAIN"
FULLCHAIN="$LIVE_DIR/fullchain.pem"
PRIVKEY="$LIVE_DIR/privkey.pem"

if [ -f "$FULLCHAIN" ] && [ -f "$PRIVKEY" ]; then
  echo "[certbot-init] Certificates already present for $PRIMARY_DOMAIN; skipping issuance."
  exit 0
fi

# Ensure directories exist
mkdir -p /etc/letsencrypt /var/lib/letsencrypt

# Use standalone auth (binds to port 80) before nginx starts
echo "[certbot-init] Requesting certificates for: $DOMAIN_ARGS"
certbot certonly --standalone --preferred-challenges http \
  --agree-tos -m "$EMAIL" -n $TEST_FLAG $DOMAIN_ARGS || {
  echo "[certbot-init] Certbot failed; nginx may not start without certificates."
}

