from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from cmsapp.domains.models import Domain, DomainPermission
from cmsapp.domains.utils import get_user_domains


class CmsAdminSite(admin.AdminSite):
    """Custom admin site with better domain support."""
    
    site_header = "CMS Administration"
    site_title = "CMS Admin"
    index_title = "Dashboard"
    
    def index(self, request, extra_context=None):
        """Custom admin index showing user's domain access."""
        extra_context = extra_context or {}
        
        if request.user.is_active:
            if request.user.is_superuser:
                domains = Domain.objects.filter(is_active=True)
                extra_context['is_superuser'] = True
                extra_context['user_domains'] = domains
            else:
                user_domains = get_user_domains(request.user)
                
                if not user_domains.exists():
                    # User is staff but has no domain permissions
                    extra_context['warning'] = (
                        'You have not been granted access to any domains. '
                        'Contact your administrator to request access.'
                    )
                    extra_context['user_domains'] = []
                else:
                    extra_context['user_domains'] = user_domains
                
                # Get user's permissions info
                perms = DomainPermission.objects.filter(
                    user=request.user,
                    is_active=True
                ).select_related('domain')
                
                if perms.exists():
                    perm_info = []
                    for perm in perms:
                        perm_info.append({
                            'domain': perm.domain,
                            'role': perm.get_role_display(),
                            'role_slug': perm.role,
                        })
                    extra_context['permissions_info'] = perm_info
        
        return super().index(request, extra_context=extra_context)
    
    def get_app_list(self, request):
        """Filter app list based on user permissions."""
        app_list = super().get_app_list(request)
        
        # For non-superusers, filter which apps they can see
        if not request.user.is_superuser:
            user_domains = get_user_domains(request.user)
            
            # If user has no domains, they can only see limited apps
            if not user_domains.exists():
                # Filter to only show domains app
                app_list = [app for app in app_list if app['app_label'] == 'domains']
        
        return app_list
