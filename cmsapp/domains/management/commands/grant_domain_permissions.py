from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from cmsapp.domains.models import DomainPermission


class Command(BaseCommand):
    help = 'Grant Django model permissions to users based on their domain permissions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Specific username to grant permissions to (optional)',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        
        if username:
            try:
                users = [User.objects.get(username=username)]
                self.stdout.write(f"Processing user: {username}")
            except User.DoesNotExist:
                self.stderr.write(self.style.ERROR(f'User "{username}" does not exist'))
                return
        else:
            # Get all users with domain permissions
            user_ids = DomainPermission.objects.filter(is_active=True).values_list('user_id', flat=True).distinct()
            users = User.objects.filter(id__in=user_ids)
            self.stdout.write(f"Processing {users.count()} users with domain permissions")
        
        for user in users:
            self.stdout.write(f"\n{'='*60}")
            self.stdout.write(f"User: {user.username}")
            self.stdout.write(f"{'='*60}")
            
            # Ensure user is staff
            if not user.is_staff:
                user.is_staff = True
                user.save(update_fields=['is_staff'])
                self.stdout.write(self.style.SUCCESS("✓ Set is_staff = True"))
            
            # Get user's domain permissions
            domain_perms = DomainPermission.objects.filter(user=user, is_active=True)
            
            if not domain_perms.exists():
                self.stdout.write(self.style.WARNING("⚠️  No active domain permissions found"))
                continue
            
            # Determine highest role
            roles = list(domain_perms.values_list('role', flat=True))
            if 'admin' in roles:
                role = 'admin'
            elif 'editor' in roles:
                role = 'editor'
            else:
                role = 'viewer'
            
            self.stdout.write(f"Highest role: {role}")
            
            # Define models to grant permissions for
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
            
            granted_count = 0
            
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
                                granted_count += 1
                            except Permission.DoesNotExist:
                                pass
                                
                    except ContentType.DoesNotExist:
                        pass
            
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
                                granted_count += 1
                            except Permission.DoesNotExist:
                                pass
                except ContentType.DoesNotExist:
                    pass
            
            self.stdout.write(self.style.SUCCESS(f"✓ Granted {granted_count} permissions"))
            
            # Show domains
            for perm in domain_perms:
                self.stdout.write(f"  - {perm.domain.name} ({perm.get_role_display()})")
        
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(self.style.SUCCESS("\n✓ Permission grant complete!"))
        self.stdout.write("\nUsers should now:")
        self.stdout.write("1. Log out of the admin interface")
        self.stdout.write("2. Clear browser cache/cookies")
        self.stdout.write("3. Log back in")
        self.stdout.write(f"{'='*60}\n")
