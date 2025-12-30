from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def health_check(request):
    """API health check endpoint."""
    return JsonResponse({
        'status': 'healthy',
        'service': 'CMS API'
    })


@login_required
def logout_view(request):
    """Logout view that handles POST requests."""
    if request.method == 'POST':
        logout(request)
        return redirect('pages:homepage')
    return redirect('pages:homepage')
