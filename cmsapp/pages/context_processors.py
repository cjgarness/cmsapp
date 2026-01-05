"""
Context processors for the pages app.
These add variables to all template contexts.
"""
from django.utils import timezone
from .models import Page
from cmsapp.domains.models import DomainSetting


def navbar_pages(request):
    """Add navbar pages to all template contexts."""
    domain = getattr(request, 'domain', None)
    navbar_qs = Page.objects.filter(show_in_navbar=True, status='published')
    if domain:
        navbar_qs = navbar_qs.filter(domain=domain)

    show_pages_link = True
    if domain:
        try:
            show_pages_link = domain.settings.show_pages_link
        except DomainSetting.DoesNotExist:
            show_pages_link = True
    
    return {
        'navbar_pages': navbar_qs,
        'current_year': timezone.now().year,
        'show_pages_link': show_pages_link,
    }
