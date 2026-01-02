from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from cmsapp.domains.models import Domain, DomainPermission


class Command(BaseCommand):
    help = 'Check domain permissions for a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to check permissions for')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')
        
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(f"Checking permissions for user: {user.username}")
        self.stdout.write(f"{'='*60}\n")
        
        # Check if user is staff
        if not user.is_staff:
            self.stdout.write(self.style.WARNING(
                f"⚠️  User is NOT a staff member. They cannot access admin console."
            ))
            self.stdout.write("Run: python manage.py shell")
            self.stdout.write("Then: User.objects.filter(username='{}').update(is_staff=True)".format(username))
        else:
            self.stdout.write(self.style.SUCCESS("✓ User is a staff member"))
        
        # Check if user is superuser
        if user.is_superuser:
            self.stdout.write(self.style.SUCCESS("✓ User is a superuser (has access to everything)"))
            self.stdout.write("")
            return
        
        # Check domain permissions
        self.stdout.write("Domain Permissions:")
        permissions = DomainPermission.objects.filter(user=user)
        
        if not permissions.exists():
            self.stdout.write(self.style.ERROR(
                "✗ User has NO domain permissions assigned!"
            ))
            self.stdout.write("\nTo assign a domain to this user:")
            self.stdout.write("1. Go to Django Admin > Domain Management > Domain Permissions")
            self.stdout.write("2. Click 'Add Domain Permission'")
            self.stdout.write(f"3. Select user '{username}'")
            self.stdout.write("4. Select a domain")
            self.stdout.write("5. Set role to 'Editor' or 'Admin'")
            self.stdout.write("6. Make sure 'is_active' is checked")
        else:
            for perm in permissions:
                active = "✓" if perm.is_active else "✗"
                self.stdout.write(f"{active} Domain: {perm.domain.name} | Role: {perm.role} | Active: {perm.is_active}")
        
        # List all available domains
        self.stdout.write("\nAvailable Domains:")
        domains = Domain.objects.filter(is_active=True)
        if domains.exists():
            for domain in domains:
                self.stdout.write(f"  - {domain.name} ({domain.title})")
        else:
            self.stdout.write(self.style.ERROR("  No active domains found!"))
        
        self.stdout.write(f"\n{'='*60}\n")
