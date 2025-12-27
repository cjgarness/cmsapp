#!/bin/bash

# SSH Reverse Port Forwarding Script
# This script forwards remote ports 80 and 443 to your local workstation
# allowing the remote host to access your local web services

# Configuration
REMOTE_USER="root"
REMOTE_HOST="rvscope.com"
LOCAL_PORT_HTTP=80
LOCAL_PORT_HTTPS=443
REMOTE_PORT_HTTP=80
REMOTE_PORT_HTTPS=443

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}SSH Reverse Port Forwarding${NC}"
echo "================================"
echo -e "Remote: ${YELLOW}${REMOTE_USER}@${REMOTE_HOST}${NC}"
echo -e "Forwarding remote port ${REMOTE_PORT_HTTP} -> local ${LOCAL_PORT_HTTP}"
echo -e "Forwarding remote port ${REMOTE_PORT_HTTPS} -> local ${LOCAL_PORT_HTTPS}"
echo "================================"
echo ""
echo -e "${YELLOW}Note: Remote SSH server must have GatewayPorts enabled${NC}"
echo ""

# Check if GatewayPorts is configured on remote server
check_gateway_ports() {
    echo "Checking GatewayPorts configuration on remote server..."
    ssh ${REMOTE_USER}@${REMOTE_HOST} "grep -q 'GatewayPorts yes' /etc/ssh/sshd_config && echo 'GatewayPorts is enabled' || echo 'GatewayPorts is NOT enabled - please configure'"
    echo ""
}

# Optionally run configuration check
if [[ "${1}" == "--check" ]]; then
    check_gateway_ports
    exit 0
fi

if [[ "${1}" == "--setup" ]]; then
    echo -e "${YELLOW}Setting up GatewayPorts on remote server...${NC}"
    ssh ${REMOTE_USER}@${REMOTE_HOST} "sudo sed -i 's/#GatewayPorts no/GatewayPorts yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh && echo 'GatewayPorts enabled and SSH restarted'"
    exit 0
fi

echo "Starting SSH reverse port forwarding..."
echo ""

# SSH with reverse port forwarding on all network interfaces
# -R [bind_address:]remote_port:local_host:local_port
# Requires GatewayPorts yes in remote /etc/ssh/sshd_config
ssh -R 172.238.164.179:${REMOTE_PORT_HTTP}:localhost:${LOCAL_PORT_HTTP} \
    -R 172.238.164.179:${REMOTE_PORT_HTTPS}:localhost:${LOCAL_PORT_HTTPS} \
    ${REMOTE_USER}@${REMOTE_HOST}

# Alternative with keep-alive and auto-reconnect:
# Uncomment the lines below and comment out the SSH command above if you want persistent connection
# while true; do
#     ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 \
#         -R 0.0.0.0:${REMOTE_PORT_HTTP}:localhost:${LOCAL_PORT_HTTP} \
#         -R 0.0.0.0:${REMOTE_PORT_HTTPS}:localhost:${LOCAL_PORT_HTTPS} \
#         ${REMOTE_USER}@${REMOTE_HOST}
#     echo -e "${RED}Connection lost. Reconnecting in 5 seconds...${NC}"
#     sleep 5
# done
