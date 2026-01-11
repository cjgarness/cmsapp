from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from cmsapp.domains.models import DomainSetting
from .models import ContactInquiry, ContactConfiguration
from .forms import ContactForm


@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact form view with domain-specific templates."""
    config = ContactConfiguration.get_config()
    domain = getattr(request, 'domain', None)
    domain_settings = None
    if domain:
        domain_settings, _ = DomainSetting.objects.get_or_create(domain=domain)
    print('Configuration:')
    print(config)
    
    # Check if contact form is enabled
    if not config.enable_contact_form:
        messages.error(request, 'The contact form is currently unavailable. Please try again later.')
        return redirect('pages:homepage')
    
    if request.method == 'POST':
        form = ContactForm(request.POST, domain=domain)
        if form.is_valid():
            # Save the inquiry to database
            inquiry = form.save(commit=False)
            inquiry.domain = domain  # Set the domain
            inquiry.save()
            
            # Send confirmation email to inquirer if enabled
            if config.send_confirmation_email:
                inquiry.send_confirmation_email()
            
            # Send alert email to admin if enabled
            inquiry.send_alert_email(config, domain, domain_settings)
            
            # Send SMS notification if enabled
            inquiry.send_sms_notification(config, domain, domain_settings)
            
            # Show success message
            messages.success(
                request,
                f'Thank you {inquiry.name}! Your inquiry has been received. '
                f'We will respond to {inquiry.email} as soon as possible.'
            )
            return redirect('contact:thank_you')
    else:
        form = ContactForm(domain=domain)
    
    context = {
        'form': form,
        'page_title': 'Contact Us',
    }
    
    # Use domain-specific template
    if domain and domain.name == 'rvscope.com':
        return render(request, 'rvscope/contact.html', context)
    
    return render(request, 'modern/contact.html', context)


def thank_you(request):
    """Thank you page after successful contact form submission."""
    domain = getattr(request, 'domain', None)
    if domain and domain.name == 'rvscope.com':
        return render(request, 'rvscope/thank_you.html', {
            'page_title': 'Thank You',
        })
    return render(request, 'modern/thank_you.html', {
        'page_title': 'Thank You',
    })

