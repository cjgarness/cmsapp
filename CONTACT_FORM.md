# Contact Form Module

A comprehensive contact form system for the CMS application that allows site visitors to submit inquiries.

## Features

- **Contact Form**: Multi-field form for inquiries (name, email, phone, company, inquiry type, subject, message)
- **Database Storage**: All inquiries automatically saved to PostgreSQL database
- **Email Notifications**: 
  - Automatic confirmation emails to inquirers
  - Admin notifications when new inquiries received
- **Admin Panel**: Full Django admin interface to manage inquiries
  - View, filter, and search inquiries
  - Mark inquiries as read/responded/closed
  - Add admin notes
  - Status tracking with color-coded badges
- **SMS Support**: Optional SMS notification integration (Twilio-ready)
- **Configurable Settings**: Enable/disable form, customize email settings, configure SMS

## Installation

1. The contact app is already integrated into the CMS application
2. Run migrations to create database tables:
   ```bash
   ./migrate.sh dev migrate
   # or for production:
   ./migrate.sh prod migrate
   ```

3. Initialize contact configuration:
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py init_contact_config
   ```

## Configuration

### Via Environment Variables

Set these in your `.env` file or Docker environment:

```bash
CONTACT_ADMIN_EMAIL=admin@example.com
ADMIN_NAME=Admin
DEFAULT_FROM_EMAIL=noreply@example.com
```

### Via Django Admin

1. Navigate to `/admin/contact/contactconfiguration/`
2. Update the settings:
   - **Admin Email**: Where new inquiries will be sent
   - **Admin Name**: Display name in email signatures
   - **Send Confirmation Emails**: Enable/disable auto-response to inquirers
   - **Enable Contact Form**: Toggle form availability
   - **SMS Notifications**: Configure Twilio for SMS alerts (optional)

## Email Configuration

For the contact form to send emails, configure your email backend in `settings.py`:

### Development (Console Backend)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@example.com'
```

### Production (SMTP)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@example.com'
```

Or set via environment variables:
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@example.com
```

## SMS Notifications (Optional)

To enable SMS notifications using Twilio:

1. Create a Twilio account at https://www.twilio.com/
2. Get your API credentials
3. In Django Admin, enable SMS notifications and add:
   - Phone number to receive SMS (format: +1234567890)
   - Twilio API key
4. Install Twilio package (optional):
   ```bash
   pip install twilio
   ```

## URLs

- **Contact Form**: `/contact/`
- **Thank You Page**: `/contact/thank-you/`
- **Admin Interface**: `/admin/contact/`

## Contact Form Fields

1. **Name** (required): Full name of inquirer
2. **Email** (required): Contact email address
3. **Phone** (optional): Contact phone number
4. **Company** (optional): Company name
5. **Inquiry Type** (required): 
   - General Question
   - Service Inquiry
   - Support Request
   - Feedback
   - Partnership Inquiry
   - Other
6. **Subject** (required): Subject of inquiry
7. **Message** (required): Detailed message

## Admin Features

### Inquiry List View
- View all inquiries with status badges
- Filter by status, type, and date
- Search by name, email, subject, or message
- Color-coded status indicators:
  - 🔴 New (red)
  - 🟠 Read (orange)
  - 🟢 Responded (green)
  - ⚪ Closed (gray)

### Actions
- Mark as Read
- Mark as Responded
- Mark as Closed
- Add admin notes for internal tracking

### Inquiry Details
- View complete inquiry information
- Add admin notes
- Update status
- See timestamps for when inquiry was read/responded

## Database Models

### ContactInquiry
- Stores all contact form submissions
- Tracks status and timestamps
- Includes admin notes field
- Automatically generates indices for performance

### ContactConfiguration
- Single configuration object for the contact system
- Stores email and SMS settings
- Controls form availability

## Customization

### Modify Form Fields
Edit `/cmsapp/contact/forms.py` to add/remove fields

### Customize Email Templates
Edit email sending in `/cmsapp/contact/views.py` function `send_admin_notification()`

### Customize Contact Page
Edit template at `/templates/contact/contact.html`

### Customize Thank You Page
Edit template at `/templates/contact/thank_you.html`

## Troubleshooting

### Emails not sending?
1. Check email configuration in settings.py
2. Verify `DEFAULT_FROM_EMAIL` is set
3. For Gmail, use App Passwords instead of regular password
4. Check Django logs for email errors

### SMS not working?
1. Verify Twilio credentials in admin
2. Ensure phone number is in correct format: +1234567890
3. Check Twilio account has sufficient credits

### Form not appearing?
1. Ensure `enable_contact_form` is True in admin
2. Check URL configuration - should be at `/contact/`
3. Verify contact app is in INSTALLED_APPS

## Support

For issues or questions about the contact form functionality, refer to the Django documentation or contact the development team.
