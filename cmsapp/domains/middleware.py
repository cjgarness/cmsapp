from cmsapp.domains.models import Domain


class DomainMiddleware:
    """Middleware to detect and set the current domain based on the request host."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get the host from the request
        host = request.get_host().split(':')[0]  # Remove port if present
        
        # Try to find a matching domain
        try:
            domain = Domain.objects.get(name=host, is_active=True)
        except Domain.DoesNotExist:
            # Try to find a domain without subdomain
            # e.g., if host is 'www.example.com', try 'example.com'
            if host.startswith('www.'):
                host_without_www = host[4:]
                try:
                    domain = Domain.objects.get(name=host_without_www, is_active=True)
                except Domain.DoesNotExist:
                    # Fall back to default domain
                    domain = Domain.objects.filter(name='altuspath.com', is_active=True).first()
            else:
                # Fall back to default domain
                domain = Domain.objects.filter(name='altuspath.com', is_active=True).first()
        
        # If still no domain found, try to get any active domain as last resort
        if not domain:
            domain = Domain.objects.filter(is_active=True).first()
        
        # Attach domain to request
        request.domain = domain
        
        response = self.get_response(request)
        return response
