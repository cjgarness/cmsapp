# ProtonMail Bridge Setup Guide

This guide explains how to configure the ProtonMail Bridge Docker container for sending confirmation emails through your ProtonMail account.

## Prerequisites

- A ProtonMail account
- Docker and Docker Compose installed
- The application containers running with `docker-compose up -d`

## ✅ Password Manager (pass) Already Installed

Good news! The Docker image now includes the `pass` password manager, which is required by ProtonMail Bridge for secure credential storage. The password store is automatically initialized on container startup, so you can skip directly to authentication.

## Setup Steps

### 1. Authenticate with ProtonMail

The ProtonMail Bridge container needs to be configured with your ProtonMail credentials. Follow these steps:

#### Interactive Setup (Recommended)

1. Access the ProtonMail Bridge CLI:
```bash
docker exec -it cmsapp_protomail_dev protonmail-bridge --cli
```

2. In the CLI, authenticate with your ProtonMail account:
```
login
# Enter your ProtonMail email
# Enter your ProtonMail password
# If you have 2FA, enter the code when prompted
```

3. List configured accounts to verify:
```
info
```

4. Exit the CLI:
```
quit
```

5. The configuration will be persisted in the Docker volume `protomail_data`

### 2. Email Configuration in Django

The Django settings are already configured to use ProtonMail Bridge:

- **Email Host**: `protomail` (Docker service name)
- **Email Port**: `1025` (SMTP)
- **Email Use TLS**: `False`

These values are set in `cmsapp/settings.py`:
```python
EMAIL_HOST = config('EMAIL_HOST', default='protomail')
EMAIL_PORT = config('EMAIL_PORT', default=1025, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='contact@example.com')
```

### 3. Set Email Address in Environment

Update your `.env` file with your ProtonMail email:
```bash
DEFAULT_FROM_EMAIL=your-protonmail@email.com
```

### 4. Test Email Sending

Test that emails are being sent properly:

```bash
# Access Django shell
docker exec -it cmsapp_web_dev python manage.py shell

# In the shell:
from django.core.mail import send_mail
send_mail(
    'Test Subject',
    'This is a test message from ProtonMail Bridge',
    'your-protonmail@email.com',
    ['recipient@example.com'],
)
# Should return 1 if successful
```

### 5. Verify Bridge Status

Check if the ProtonMail Bridge is running and listening:

```bash
# Check bridge logs
docker logs cmsapp_protomail_dev

# Test SMTP connection
docker exec cmsapp_web_dev nc -zv protomail 1025

# Verify pass password store
docker exec cmsapp_protomail_dev bash -c 'export PASSWORD_STORE_DIR=/home/protonmail/.password-store; pass ls'
```

## Troubleshooting

### Bridge Not Connected/Authenticated

If you see authentication errors in logs:
- The bridge needs to be authenticated with ProtonMail credentials
- Follow the Interactive Setup steps above
- Make sure 2FA codes are entered correctly if enabled

### SMTP Connection Refused

If contact form submissions fail with SMTP errors:
1. Verify the bridge container is running: `docker ps | grep protomail`
2. Check bridge logs: `docker logs cmsapp_protomail_dev`
3. Ensure web container can reach the bridge: `docker exec cmsapp_web_dev nc -zv protomail 1025`
4. Verify bridge is authenticated: look for a "Connected" status in `docker exec -it cmsapp_protomail_dev protonmail-bridge --cli` (then type `info`)

### Password Manager Issues

The `pass` password manager is now automatically initialized in the Docker image. If you see password manager errors:

```bash
# Check if pass is initialized
docker exec cmsapp_protomail_dev bash -c 'export PASSWORD_STORE_DIR=/home/protonmail/.password-store; pass ls'

# Reinitialize password store
docker exec cmsapp_protomail_dev bash -c 'rm -rf /home/protonmail/.password-store && /usr/local/bin/init-pass.sh'

# Then restart the container
docker restart cmsapp_protomail_dev
```

### Configuration Persistence

The bridge configuration is stored in the Docker volume `protomail_data`. If you delete this volume, you'll need to re-authenticate:
```bash
docker volume rm cmsapp_protomail_data
docker-compose up -d protomail
# Then follow setup steps again
```

## Docker Image Details

The `cmsapp-protomail` Docker image extends the official `shenxn/protonmail-bridge` image and adds:

- **pass** password manager for credential storage
- **GPG 2.4.8** for encryption
- Automatic initialization scripts for GPG and pass
- Environment variables for seamless integration

### Installed Components

- `pass 1.7.4` - Password store management
- `gnupg2 2.4.8` - GPG suite  
- `gpg` - GNU Privacy Guard
- `pwgen` - Secure password generator
- `expect` - Automation tool for interactive applications

## Security Notes

1. **Credentials**: ProtonMail Bridge stores encrypted credentials in the volume. Never commit this volume to version control.
2. **Password Manager**: The `pass` password manager stores encrypted passwords. Access is controlled by GPG.
3. **Network**: The SMTP port (1025) is only exposed to other containers on the internal Docker network, not to the host.
4. **Volumes**: Three volumes are used:
   - `protomail_data` - ProtonMail Bridge configuration
   - `protomail_gnupg` - GPG keys and trustdb
   - `protomail_pass` - Password store data

## Reference

- [ProtonMail Bridge Documentation](https://proton.me/support/mail-bridge)
- [shenxn/protonmail-bridge Docker Image](https://github.com/shenxn/protonmail-bridge-docker)
- [pass Password Manager](https://www.passwordstore.org/)
- [Django Email Configuration](https://docs.djangoproject.com/en/stable/topics/email/)
