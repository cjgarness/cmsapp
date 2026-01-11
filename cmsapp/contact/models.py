from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from cmsapp.domains.models import Domain


class InquiryType(models.Model):
    """Inquiry type options manageable per domain."""
    
    domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE,
        related_name='inquiry_types'
    )
    slug = models.SlugField(
        max_length=50,
        help_text="Internal identifier for this inquiry type"
    )
    label = models.CharField(
        max_length=100,
        help_text="Display name for this inquiry type"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order in dropdown"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Enable/disable this inquiry type"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'label']
        unique_together = ('domain', 'slug')
        verbose_name_plural = 'Inquiry Types'
        indexes = [
            models.Index(fields=['domain', 'is_active']),
        ]
    
    def __str__(self):
        return self.label


class ContactInquiry(models.Model):
    """Model to store contact form submissions."""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('responded', 'Responded'),
        ('closed', 'Closed'),
    ]
    
    # Contact information
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Inquiry details
    domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE,
        related_name='contact_inquiries',
        null=True,
        blank=True
    )
    inquiry_type = models.ForeignKey(
        InquiryType,
        on_delete=models.PROTECT,
        related_name='inquiries',
        null=True,
        blank=True
    )
    # DEPRECATED: keeping old inquiry_type CharField for backwards compatibility
    # This is now the inquiry_type above (ForeignKey)
    message = models.TextField()
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_at = models.DateTimeField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    # Admin notes
    admin_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact Inquiries'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['domain', 'status']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.inquiry_type.label} ({self.domain.name})"
    
    def mark_as_read(self):
        """Mark inquiry as read."""
        if self.status == 'new':
            self.status = 'read'
            self.read_at = timezone.now()
            self.save()
    
    def send_confirmation_email(self):
        """Send confirmation email to the inquirer."""
        try:
            subject = f"We received your {self.inquiry_type.label.lower()} inquiry"
            message = f"""
Dear {self.name},

Thank you for contacting us! We have received your inquiry and will get back to you as soon as possible.

Inquiry Details:
- Type: {self.inquiry_type.label}
- Date: {self.created_at.strftime('%B %d, %Y at %I:%M %p')}

We appreciate your interest and look forward to assisting you.

Best regards,
The {settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else 'CMS'} Team
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

    def send_alert_email(self, config, domain=None, domain_settings=None):
        """Send email alert to admin about new inquiry."""
        print('Sending alert email...')

        # Domain-level toggle and email take precedence when available
        domain_email_enabled = domain_settings.enable_alert_email if domain_settings else False
        domain_email = self.domain.contact_email if self.domain else None

        if domain_settings is not None:
            if not domain_email_enabled or not domain_email:
                print('Domain email alerts disabled or email not set; skipping')
                return False
            recipient_email = domain_email
        else:
            if not config.admin_email:
                print('Admin email not configured')
                return False
            recipient_email = config.admin_email

        try:
            subject = f"New {self.inquiry_type.label} Inquiry from {self.name}"
            message = f"""
A new inquiry has been submitted:

From: {self.name}
Email: {self.email}
Phone: {self.phone or 'Not provided'}
Type: {self.inquiry_type.label}
Date: {self.created_at.strftime('%B %d, %Y at %I:%M %p')}

Message:
{self.message}

---
You can review this inquiry in the admin panel.
            """

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=True,
            )
            print(f"Alert email sent to {recipient_email}")
            return True
        except Exception as e:
            print(f"Error sending alert email: {e}")
            return False

    def send_sms_notification(self, config, domain=None, domain_settings=None):
        """Send SMS alert to admin about new inquiry using Twilio."""
        print('Sending SMS notification...')

        # Domain-level toggle and phone take precedence when available
        domain_sms_enabled = domain_settings.enable_alert_sms if domain_settings else False
        domain_phone = self.domain.contact_phone if self.domain else None

        if domain_settings is not None:
            if not domain_sms_enabled or not domain_phone:
                print('Domain SMS alerts disabled or phone not set; skipping')
                return False
            target_number = domain_phone
        else:
            if not config.enable_sms_notifications or not config.sms_phone_number:
                print('SMS notifications not enabled or phone number not configured')
                return False
            target_number = config.sms_phone_number

        # Check Twilio credentials
        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN or not settings.TWILIO_PHONE_NUMBER:
            print('Twilio credentials not configured in settings')
            return False

        try:
            from twilio.rest import Client

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            sms_body = (
                f"New {self.inquiry_type.label} from {self.name}\n"
                f"Email: {self.email}\n"
                f"Check admin panel for details."
            )

            message = client.messages.create(
                body=sms_body,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=target_number
            )

            print(f"SMS sent successfully. SID: {message.sid}")
            return True

        except ImportError:
            print("Twilio package not installed. Run: pip install twilio")
            return False
        except Exception as e:
            print(f"Error sending SMS notification: {e}")
            return False


class ContactConfiguration(models.Model):
    """Configuration for contact form notifications."""
    
    # Email settings
    admin_email = models.EmailField(
        help_text="Email address where inquiries will be sent"
    )
    admin_name = models.CharField(
        max_length=200,
        default="Admin",
        help_text="Name to display in email signatures"
    )
    send_confirmation_email = models.BooleanField(
        default=True,
        help_text="Send confirmation emails to inquirers"
    )
    
    # SMS settings (optional)
    enable_sms_notifications = models.BooleanField(
        default=False,
        help_text="Enable SMS notifications for new inquiries"
    )
    sms_phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Phone number to receive SMS notifications (Twilio format: +1234567890)"
    )
    sms_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Twilio API key (stored securely)"
    )
    
    # General settings
    enable_contact_form = models.BooleanField(
        default=True,
        help_text="Enable or disable the contact form"
    )
    auto_response_enabled = models.BooleanField(
        default=True,
        help_text="Send automatic responses to inquiries"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Contact Configuration'
        verbose_name_plural = 'Contact Configuration'
    
    def __str__(self):
        sms_status = "Enabled" if self.enable_sms_notifications else "Disabled"
        confirmation_status = "Enabled" if self.send_confirmation_email else "Disabled"
        form_status = "Enabled" if self.enable_contact_form else "Disabled"
        auto_response_status = "Enabled" if self.auto_response_enabled else "Disabled"
        
        return (
            f"Contact Configuration | "
            f"Admin: {self.admin_name} ({self.admin_email}) | "
            f"Form: {form_status} | "
            f"Confirmations: {confirmation_status} | "
            f"Auto-response: {auto_response_status} | "
            f"SMS: {sms_status}" +
            (f" ({self.sms_phone_number})" if self.enable_sms_notifications and self.sms_phone_number else "") +
            f" | Updated: {self.updated_at.strftime('%B %d, %Y')}"
        )
    
    @classmethod
    def get_config(cls):
        """Get or create contact configuration."""
        config, _ = cls.objects.get_or_create(pk=1)
        return config
