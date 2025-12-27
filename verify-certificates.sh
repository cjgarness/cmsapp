#!/bin/bash
# Verify and report on current SSL certificates in use

LETSENCRYPT_CERT="/etc/letsencrypt/live/rvscope.com/fullchain.pem"
NGINX_CONTAINER="cmsapp-nginx-prod"

echo "======================================"
echo "SSL Certificate Verification"
echo "======================================"
echo ""

# Check if Let's Encrypt cert exists on host
if [ -f "$LETSENCRYPT_CERT" ]; then
    echo "✓ Let's Encrypt certificate found on host"
    echo "  Path: $LETSENCRYPT_CERT"
    
    # Get cert info
    CERT_INFO=$(openssl x509 -in "$LETSENCRYPT_CERT" -text -noout)
    SUBJECT=$(echo "$CERT_INFO" | grep "Subject:" | head -1)
    ISSUER=$(echo "$CERT_INFO" | grep "Issuer:" | head -1)
    NOT_BEFORE=$(echo "$CERT_INFO" | grep "Not Before:" | head -1)
    NOT_AFTER=$(echo "$CERT_INFO" | grep "Not After:" | head -1)
    
    echo "  $SUBJECT"
    echo "  $ISSUER"
    echo "  $NOT_BEFORE"
    echo "  $NOT_AFTER"
else
    echo "✗ Let's Encrypt certificate NOT found"
fi

echo ""
echo "Checking certificate in running Nginx container..."

# Get the certificate that Nginx is actually serving
if docker compose -f docker-compose.prod.yml ps nginx &>/dev/null; then
    # Extract the actual certificate from nginx
    NGINX_CERT=$(docker compose -f docker-compose.prod.yml exec -T nginx openssl s_client -showcerts -connect localhost:443 </dev/null 2>/dev/null | openssl x509 -text 2>/dev/null || true)
    
    if [ -z "$NGINX_CERT" ]; then
        echo "Could not retrieve certificate from Nginx"
    else
        NGINX_SUBJECT=$(echo "$NGINX_CERT" | grep "Subject:" | head -1)
        NGINX_ISSUER=$(echo "$NGINX_CERT" | grep "Issuer:" | head -1)
        echo "Certificate currently served by Nginx:"
        echo "  $NGINX_SUBJECT"
        echo "  $NGINX_ISSUER"
        
        # Determine if it's self-signed or from Let's Encrypt
        if echo "$NGINX_ISSUER" | grep -q "Let's Encrypt"; then
            echo "  ✓ Currently using Let's Encrypt certificate"
        elif echo "$NGINX_ISSUER" | grep -q "self-signed"; then
            echo "  ⚠ Currently using self-signed certificate"
            echo ""
            echo "ACTION REQUIRED:"
            echo "If Let's Encrypt certificates have been issued, reload Nginx:"
            echo "  docker compose -f docker-compose.prod.yml exec -T nginx nginx -s reload"
        fi
    fi
else
    echo "Nginx container not running"
fi

echo ""
echo "======================================"
