# Contact Form Module - Quick Start

## What was created?

A complete contact form system with the following components:

### Database Models
- **ContactInquiry**: Stores visitor inquiries with status tracking
- **ContactConfiguration**: Manages contact form settings

### Features
✅ Contact form for visitors to submit inquiries  
✅ Inquiry types: General Question, Service Inquiry, Support Request, Feedback, Partnership, Other  
✅ Database storage of all submissions  
✅ Automatic email confirmations to users  
✅ Admin notifications when new inquiries arrive  
✅ Django admin interface to manage inquiries  
✅ Status tracking: New → Read → Responded → Closed  
✅ SMS notification support (optional, Twilio-ready)  
✅ Configurable email settings  

### URLs
- `/contact/` - Contact form page
- `/contact/thank-you/` - Thank you page
- `/admin/contact/` - Admin interface

## Getting Started

### 1. Run Migrations
```bash
./migrate.sh dev migrate
# or production:
./migrate.sh prod migrate
```

### 2. Initialize Contact Configuration
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py init_contact_config
```

Or for production:
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py init_contact_config
```

### 3. Configure Email Settings

Set environment variables in your `.env` or docker-compose file:

```bash
CONTACT_ADMIN_EMAIL=admin@yoursite.com
ADMIN_NAME=Your Name
DEFAULT_FROM_EMAIL=noreply@yoursite.com
```

### 4. Update Admin Settings
Navigate to `/admin/contact/contactconfiguration/` and update:
- Admin email address
- Enable/disable confirmation emails
- Configure SMS (optional)

## Email Configuration

For emails to work, configure your email backend. Example for Gmail:

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password for Gmail
DEFAULT_FROM_EMAIL = 'noreply@yoursite.com'
```

Or set via environment variables - they'll be loaded automatically.

## Files Created

```
cmsapp/contact/
├── __init__.py
├── admin.py              # Django admin configuration
├── apps.py               # App configuration
├── forms.py              # Contact form
├── models.py             # ContactInquiry & ContactConfiguration models
├── tests.py              # Unit tests
├── urls.py               # URL routing
├── views.py              # Contact views
├── management/
│   └── commands/
│       └── init_contact_config.py  # Setup command
└── migrations/
    └── 0001_initial.py   # Database migrations

templates/contact/
├── contact.html          # Contact form page
└── thank_you.html        # Thank you page

CONTACT_FORM.md           # Full documentation
```

## Testing

Run tests to verify everything works:

```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py test cmsapp.contact
```

## Admin Features

In Django admin at `/admin/contact/contactinquiry/`:

- **View inquiries** with color-coded status badges
- **Filter** by status, type, date range
- **Search** by name, email, subject, message
- **Actions**: Mark as Read, Mark as Responded, Mark as Closed
- **Add notes** for internal team communication
- **Track** when inquiries were read and responded to

## SMS Notifications (Optional)

To add SMS notifications:

1. Create Twilio account: https://www.twilio.com/
2. Get API credentials
3. In Django admin, set:
   - Enable SMS notifications
   - Add phone number (format: +1234567890)
   - Add Twilio API key
4. Install Twilio: `pip install twilio`

## Contact Inquiry Flow

```
User submits form
    ↓
Inquiry saved to database
    ↓
Confirmation email sent to user (if enabled)
    ↓
Admin notification email sent
    ↓
Admin sees "New" inquiry in admin panel
    ↓
Admin clicks "Mark as Read"
    ↓
Admin responds and "Mark as Responded"
    ↓
Admin "Mark as Closed" when done
```

## Customization

### Add new inquiry types
Edit `models.py`, INQUIRY_TYPE_CHOICES in ContactInquiry model

### Modify form fields
Edit `forms.py` ContactForm class

### Change confirmation email text
Edit `views.py`, send_admin_notification() function

### Update contact page styling
Edit `templates/contact/contact.html`

## Troubleshooting

**Emails not sending?**
- Check DEFAULT_FROM_EMAIL is set
- Verify SMTP credentials if using SMTP
- Check Django logs for errors
- For Gmail, use App Password instead of regular password

**Form not appearing?**
- Verify `enable_contact_form = True` in admin
- Check URL routing: should be at `/contact/`
- Verify contact app is in INSTALLED_APPS

**SMS not working?**
- Verify Twilio credentials
- Phone format must be: +1234567890
- Check Twilio account has sufficient credits

## Next Steps

1. Customize the contact form page design
2. Add custom email templates for branded emails
3. Set up Twilio SMS notifications for critical inquiries
4. Configure automated responses for specific inquiry types
5. Add analytics to track inquiry types and response rates

## Support

For full documentation, see [CONTACT_FORM.md](CONTACT_FORM.md)
