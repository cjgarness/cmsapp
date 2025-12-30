# Contact Form Configuration Examples

## Email Configuration

### Option 1: Gmail with App Password (Recommended for Development)

```python
# settings.py or via environment variables

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-character-app-password'
DEFAULT_FROM_EMAIL = 'noreply@yoursite.com'
```

**Setup Steps:**
1. Enable 2-Factor Authentication on Gmail account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Copy the 16-character password
4. Add to settings or environment variables

### Option 2: SendGrid (Recommended for Production)

```python
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = 'SG.your-api-key-here'
DEFAULT_FROM_EMAIL = 'noreply@yoursite.com'
```

Install: `pip install sendgrid-django`

### Option 3: Mailgun

```python
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'your-mailgun-api-key'
MAILGUN_SERVER_NAME = 'mail.yoursite.com'
DEFAULT_FROM_EMAIL = 'noreply@yoursite.com'
```

Install: `pip install django-mailgun`

### Option 4: Development Console (Testing Only)

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@yoursite.com'
```

Emails print to console instead of sending.

### Option 5: File Backend (Testing)

```python
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/django-emails'
DEFAULT_FROM_EMAIL = 'noreply@yoursite.com'
```

Emails saved to files in specified directory.

## Environment Variables Setup

Create a `.env` file in your project root:

```bash
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yoursite.com

# Contact Form Configuration
CONTACT_ADMIN_EMAIL=admin@yoursite.com
ADMIN_NAME=Website Administrator
```

Load these in your settings.py:

```python
from decouple import config

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')
```

## Docker Compose Configuration

### Development Environment

```yaml
# docker-compose.dev.yml - Add to services.web.environment

environment:
  - EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
  - DEFAULT_FROM_EMAIL=noreply@localhost
  - CONTACT_ADMIN_EMAIL=admin@localhost
```

### Production Environment

```yaml
# docker-compose.prod.yml - Add to services.web.environment

environment:
  - EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
  - EMAIL_HOST=${EMAIL_HOST}
  - EMAIL_PORT=${EMAIL_PORT}
  - EMAIL_USE_TLS=${EMAIL_USE_TLS}
  - EMAIL_HOST_USER=${EMAIL_HOST_USER}
  - EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
  - DEFAULT_FROM_EMAIL=${DEFAULT_FROM_EMAIL}
  - CONTACT_ADMIN_EMAIL=${CONTACT_ADMIN_EMAIL}
```

## Admin Configuration Setup

After running migrations and init command:

1. Go to `/admin/contact/contactconfiguration/`
2. Set Admin Email
3. Set Admin Name
4. Enable/disable Confirmation Emails
5. (Optional) Configure SMS

## SMS Configuration (Twilio)

### Setup Steps

1. Create Twilio Account: https://www.twilio.com/
2. Get phone number and API credentials
3. Install Twilio: `pip install twilio`
4. Add to settings.py:

```python
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER', default='')
```

5. Add environment variables:

```bash
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_PHONE_NUMBER=+1234567890
```

6. In Django Admin, enable SMS and add your receiving phone number

### Sample SMS Notification Code (Optional Enhancement)

```python
from twilio.rest import Client

def send_sms_notification(inquiry, config):
    """Send SMS notification to admin about new inquiry."""
    if not config.enable_sms_notifications or not config.sms_phone_number:
        return False
    
    try:
        from django.conf import settings
        
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=f"New inquiry from {inquiry.name} ({inquiry.inquiry_type}): {inquiry.subject}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=config.sms_phone_number
        )
        return True
    except Exception as e:
        print(f"SMS notification failed: {e}")
        return False
```

## Testing Email Configuration

### Test 1: Console Output
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Submit form - emails appear in console
```

### Test 2: Django Shell
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Subject here',
    'This is a message.',
    'noreply@example.com',
    ['recipient@example.com'],
    fail_silently=False,
)
```

### Test 3: Full Contact Form Test
1. Navigate to http://localhost:8000/contact/
2. Fill out form with test data
3. Submit
4. Check admin panel for inquiry
5. Check email backend output for notification email

## Common Issues & Solutions

### Issue: Emails not sending

**Solution:**
- Verify EMAIL_BACKEND is configured
- Check DEFAULT_FROM_EMAIL is set
- For Gmail, use App Password (16 chars) not regular password
- Check Django logs: `docker-compose -f docker-compose.dev.yml logs web`
- Test email in shell (see above)

### Issue: Gmail "Less secure app access" error

**Solution:**
- Gmail disabled "Less secure apps"
- Use App Passwords instead: https://myaccount.google.com/apppasswords
- Enable 2FA first, then generate app password

### Issue: Connection refused on SMTP

**Solution:**
- Verify EMAIL_PORT is correct (usually 587 for TLS, 465 for SSL)
- Check EMAIL_USE_TLS setting matches server requirements
- Test connection: `telnet smtp.gmail.com 587`

### Issue: "Unexpected code" error with Gmail

**Solution:**
- Using regular Gmail password instead of App Password
- Generate App Password: https://myaccount.google.com/apppasswords
- Enable 2-Factor Authentication first

## Email Template Customization

Edit `cmsapp/contact/views.py` function `send_admin_notification()`:

```python
def send_admin_notification(inquiry, config):
    """Send notification email to admin about new inquiry."""
    try:
        subject = f"[New Inquiry] {inquiry.get_inquiry_type_display()}: {inquiry.subject}"
        
        message = f"""
Dear {config.admin_name},

A new contact inquiry has been received:

From: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone or 'Not provided'}
Company: {inquiry.company or 'Not provided'}
Type: {inquiry.get_inquiry_type_display()}
Received: {inquiry.created_at.strftime('%B %d, %Y at %I:%M %p')}

Subject: {inquiry.subject}

Message:
{inquiry.message}

---
Admin Link: {settings.SITE_URL}/admin/contact/contactinquiry/{inquiry.id}/change/

You can respond to this inquiry in the Django admin panel.
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [config.admin_email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending admin notification: {e}")
```

## Confirmation Email Template Customization

Edit `cmsapp/contact/models.py` method `send_confirmation_email()`:

```python
def send_confirmation_email(self):
    """Send confirmation email to the inquirer."""
    try:
        subject = f"We received your inquiry: {self.subject}"
        
        message = f"""
Dear {self.name},

Thank you for contacting us! We have received your {self.get_inquiry_type_display()}.

Your Inquiry Details:
- Date: {self.created_at.strftime('%B %d, %Y at %I:%M %p')}
- Subject: {self.subject}
- Reference: #{self.id}

We appreciate your interest and will respond as soon as possible. 
Our typical response time is 24-48 business hours.

Best regards,
{settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else 'CMS'} Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending confirmation email: {e}")
```

## Complete Working Example

Here's a complete working setup:

```python
# settings.py

from decouple import config

# Email Configuration
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')

# Site Information (for emails)
SITE_NAME = config('SITE_NAME', default='CMS')
SITE_URL = config('SITE_URL', default='http://localhost:8000')

# Contact Form Settings
CONTACT_ADMIN_EMAIL = config('CONTACT_ADMIN_EMAIL', default='admin@example.com')
```

Then set environment variables:

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yoursite.com
CONTACT_ADMIN_EMAIL=admin@yoursite.com
SITE_NAME=Your Site Name
SITE_URL=https://yoursite.com
```

This completes the setup!
