"""
Context processors for the pages app.
These add variables to all template contexts.
"""
from django.utils import timezone
from .models import Page


def navbar_pages(request):
    """Add navbar pages to all template contexts."""
    domain = getattr(request, 'domain', None)
    navbar_qs = Page.objects.filter(show_in_navbar=True, status='published')
    if domain:
        navbar_qs = navbar_qs.filter(domain=domain)
    return {
        'navbar_pages': navbar_qs,
        'current_year': timezone.now().year,
    }
