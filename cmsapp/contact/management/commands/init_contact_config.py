from django.core.management.base import BaseCommand
from cmsapp.contact.models import ContactConfiguration
import os


class Command(BaseCommand):
    help = 'Initialize contact form configuration'

    def handle(self, *args, **options):
        # Get or create configuration
        config, created = ContactConfiguration.objects.get_or_create(pk=1)
        
        if created:
            # Set defaults from environment or prompt user
            admin_email = os.getenv('CONTACT_ADMIN_EMAIL', 'admin@example.com')
            
            config.admin_email = admin_email
            config.admin_name = os.getenv('ADMIN_NAME', 'Admin')
            config.send_confirmation_email = True
            config.enable_contact_form = True
            config.auto_response_enabled = True
            config.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Contact configuration initialized!\n'
                    f'  Admin Email: {config.admin_email}\n'
                    f'  You can update settings in Django admin: /admin/contact/contactconfiguration/1/'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Contact configuration already exists.\n'
                    'To update settings, visit: /admin/contact/contactconfiguration/1/'
                )
            )
