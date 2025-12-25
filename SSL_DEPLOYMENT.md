# SSL Deployment (Let's Encrypt via Certbot)

This document describes enabling HTTPS for **rvscope.com**, **www.rvscope.com**, **altuspath.com**, and **www.altuspath.com** using the Docker Compose setup with nginx and certbot.

## Prerequisites
- DNS A/AAAA records for all four hostnames pointing to this server.
- `docker` and the Docker Compose plugin available (`docker compose version`).
- Production stack configured (see `docker-compose.prod.yml`).

## One-time certificate issuance
Run these after DNS is correct and ports 80/443 are reachable.

```bash
# Start nginx (serves ACME webroot) and certbot (renewal loop)
docker compose up -d nginx certbot

# Obtain initial certificates (prompts only if failures occur)
docker compose run --rm certbot certonly \
  --webroot -w /var/www/certbot \
  --email you@example.com --agree-tos --no-eff-email \
  -d rvscope.com -d www.rvscope.com -d altuspath.com -d www.altuspath.com

# Reload nginx to pick up the new certs
docker compose restart nginx
```

## Renewal
- The `certbot` service in `docker-compose.prod.yml` runs `certbot renew` every 12h using the shared volumes (`letsencrypt` and `certbot_challenge`).
- After a successful renewal, reload nginx to use the refreshed certs:

```bash
docker compose exec nginx nginx -s reload
# or
# docker compose restart nginx
```

## Storage and paths
- Certificates: `/etc/letsencrypt/live/rvscope.com/` (mounted into nginx from the `letsencrypt` volume).
- ACME webroot: `/var/www/certbot` (mounted from the `certbot_challenge` volume).

## Troubleshooting
- Check logs: `docker compose logs -f nginx certbot`
- Verify webroot reachability: `curl http://rvscope.com/.well-known/acme-challenge/test`
- Dry-run renewal: `docker compose run --rm certbot renew --dry-run`
