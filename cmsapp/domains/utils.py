from django.shortcuts import redirect
from functools import wraps
from .models import DomainPermission


def get_user_domains(user):
    """Get all domains a user has access to."""
    if user.is_superuser:
        from .models import Domain
        return Domain.objects.filter(is_active=True)
    
    return Domain.objects.filter(
        user_permissions__user=user,
        user_permissions__is_active=True,
        is_active=True
    ).distinct()


def get_user_permissions_for_domain(user, domain):
    """Get user's permission object for a specific domain."""
    if user.is_superuser:
        # Create a fake permission object for superusers
        class SuperuserPermission:
            role = 'admin'
            def has_edit_permission(self):
                return True
            def has_admin_permission(self):
                return True
        return SuperuserPermission()
    
    return DomainPermission.objects.filter(
        user=user,
        domain=domain,
        is_active=True
    ).first()


def require_domain_permission(permission_type='edit'):
    """
    Decorator to check if user has permission for a domain.
    permission_type can be 'view', 'edit', or 'admin'
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            domain_id = kwargs.get('domain_id') or request.GET.get('domain_id')
            
            if not domain_id:
                return redirect('admin:index')
            
            from .models import Domain
            try:
                domain = Domain.objects.get(id=domain_id, is_active=True)
            except Domain.DoesNotExist:
                return redirect('admin:index')
            
            perm = get_user_permissions_for_domain(request.user, domain)
            
            if not perm:
                return redirect('admin:index')
            
            if permission_type == 'edit' and not perm.has_edit_permission():
                return redirect('admin:index')
            elif permission_type == 'admin' and not perm.has_admin_permission():
                return redirect('admin:index')
            
            # Pass domain and permission to the view
            kwargs['domain'] = domain
            kwargs['user_permission'] = perm
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def filter_queryset_by_domain(queryset, user, domain=None):
    """
    Filter a queryset by domain based on user permissions.
    If domain is provided, only filter by that domain.
    If domain is None, filter by all domains the user has access to.
    """
    if user.is_superuser:
        if domain:
            return queryset.filter(domain=domain)
        return queryset
    
    if domain:
        perm = get_user_permissions_for_domain(user, domain)
        if perm:
            return queryset.filter(domain=domain)
        return queryset.none()
    
    user_domains = get_user_domains(user)
    return queryset.filter(domain__in=user_domains)
