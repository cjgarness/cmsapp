from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactInquiry, ContactConfiguration
from .forms import ContactForm


@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact form view."""
    config = ContactConfiguration.get_config()
    print('Configuration:')
    print(config)
    
    # Check if contact form is enabled
    if not config.enable_contact_form:
        messages.error(request, 'The contact form is currently unavailable. Please try again later.')
        return redirect('pages:homepage')
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the inquiry to database
            inquiry = form.save()
            
            # Send confirmation email to inquirer if enabled
            if config.send_confirmation_email:
                inquiry.send_confirmation_email()
            
            # Send notification email to admin
            send_admin_notification(inquiry, config)
            
            # Send SMS notification if enabled
            if config.enable_sms_notifications:
                send_sms_notification(inquiry, config)
            
            # Show success message
            messages.success(
                request,
                f'Thank you {inquiry.name}! Your inquiry has been received. '
                f'We will respond to {inquiry.email} as soon as possible.'
            )
            return redirect('contact:thank_you')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Contact Us',
    }
    return render(request, 'contact/contact.html', context)


def thank_you(request):
    """Thank you page after successful contact form submission."""
    return render(request, 'contact/thank_you.html', {
        'page_title': 'Thank You',
    })


def send_admin_notification(inquiry, config):
    print('Sending admin notification...')
    """Send notification email to admin about new inquiry."""
    try:
        subject = f"New {inquiry.get_inquiry_type_display()}: {inquiry.subject}"
        
        message = f"""
A new contact inquiry has been received:

Name: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone or 'Not provided'}
Company: {inquiry.company or 'Not provided'}
Type: {inquiry.get_inquiry_type_display()}
Subject: {inquiry.subject}

Message:
{inquiry.message}

---
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


def send_sms_notification(inquiry, config):
    """Send SMS notification to admin about new inquiry using Twilio."""
    print('Sending SMS notification...')
    if not config.enable_sms_notifications or not config.sms_phone_number:
        print('SMS notifications not enabled or phone number not configured')
        return False
    
    # Check if Twilio credentials are configured
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN or not settings.TWILIO_PHONE_NUMBER:
        print('Twilio credentials not configured in settings')
        return False
    
    try:
        from twilio.rest import Client
        
        # Initialize Twilio client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # Compose SMS message
        sms_body = (
            f"New {inquiry.get_inquiry_type_display()} from {inquiry.name}\n"
            f"Subject: {inquiry.subject}\n"
            f"Email: {inquiry.email}\n"
            f"Check admin panel for details."
        )
        
        # Send SMS
        message = client.messages.create(
            body=sms_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=config.sms_phone_number
        )
        
        print(f"SMS sent successfully. SID: {message.sid}")
        return True
        
    except ImportError:
        print("Twilio package not installed. Run: pip install twilio")
        return False
    except Exception as e:
        print(f"Error sending SMS notification: {e}")
        return False
        return False
    
    return True
