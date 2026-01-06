from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


class ContactInquiry(models.Model):
    """Model to store contact form submissions."""
    
    INQUIRY_TYPE_CHOICES = [
        ('question', 'General Question'),
        ('service', 'SSchedule Service'),
        ('feedback', 'Feedback'),
        ('other', 'Other'),
    ]
    
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
    inquiry_type = models.CharField(
        max_length=20,
        choices=INQUIRY_TYPE_CHOICES,
        default='question'
    )
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
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.get_inquiry_type_display()}"
    
    def mark_as_read(self):
        """Mark inquiry as read."""
        if self.status == 'new':
            self.status = 'read'
            self.read_at = timezone.now()
            self.save()
    
    def send_confirmation_email(self):
        """Send confirmation email to the inquirer."""
        try:
            subject = f"We received your {self.get_inquiry_type_display().lower()} inquiry"
            message = f"""
Dear {self.name},

Thank you for contacting us! We have received your inquiry and will get back to you as soon as possible.

Inquiry Details:
- Type: {self.get_inquiry_type_display()}
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
