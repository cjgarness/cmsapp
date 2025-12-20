from django.http import JsonResponse


def health_check(request):
    """API health check endpoint."""
    return JsonResponse({
        'status': 'healthy',
        'service': 'CMS API'
    })
