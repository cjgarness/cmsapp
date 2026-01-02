from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import DomainPermission


@receiver(post_save, sender=DomainPermission)
def grant_django_permissions(sender, instance, created, **kwargs):
    """
    Automatically grant Django model permissions when a DomainPermission is created or updated.
    """
    if not instance.is_active:
        return
    
    user = instance.user
    role = instance.role
    
    # Ensure user is staff
    if not user.is_staff:
        user.is_staff = True
        user.save(update_fields=['is_staff'])
    
    # Define which models this user should have access to based on role
    app_models = {
        'pages': ['page', 'pageblock', 'pageimage'],
        'media': ['mediafolder', 'mediafile', 'mediagallery'],
        'templates': ['pagetemplate', 'stylesheet', 'layoutcomponent'],
        'contact': ['contactinquiry', 'contactconfiguration'],
    }
    
    # Define permissions based on role
    if role == 'viewer':
        permission_types = ['view']
    elif role == 'editor':
        permission_types = ['view', 'add', 'change', 'delete']
    elif role == 'admin':
        permission_types = ['view', 'add', 'change', 'delete']
    else:
        permission_types = ['view']
    
    # Grant permissions for each model
    for app_label, models in app_models.items():
        for model_name in models:
            try:
                content_type = ContentType.objects.get(app_label=app_label, model=model_name)
                
                for perm_type in permission_types:
                    codename = f"{perm_type}_{model_name}"
                    try:
                        permission = Permission.objects.get(
                            content_type=content_type,
                            codename=codename
                        )
                        user.user_permissions.add(permission)
                    except Permission.DoesNotExist:
                        pass  # Permission doesn't exist for this model
                        
            except ContentType.DoesNotExist:
                pass  # Model doesn't exist
    
    # For admin role, also grant domain management permissions
    if role == 'admin':
        try:
            domain_ct = ContentType.objects.get(app_label='domains', model='domain')
            domain_setting_ct = ContentType.objects.get(app_label='domains', model='domainsetting')
            
            for ct in [domain_ct, domain_setting_ct]:
                for perm_type in ['view', 'change']:
                    codename = f"{perm_type}_{ct.model}"
                    try:
                        permission = Permission.objects.get(
                            content_type=ct,
                            codename=codename
                        )
                        user.user_permissions.add(permission)
                    except Permission.DoesNotExist:
                        pass
        except ContentType.DoesNotExist:
            pass
