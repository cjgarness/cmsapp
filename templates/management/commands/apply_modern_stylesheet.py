"""
Management command to apply modern stylesheet to a domain.
Usage: python manage.py apply_modern_stylesheet --domain altuspath.com
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from cmsapp.templates.models import Stylesheet
from cmsapp.domains.models import Domain
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Apply modern stylesheet to a domain'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            default='altuspath.com',
            help='Domain name (default: altuspath.com)',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        domain_name = options['domain']
        
        try:
            domain = Domain.objects.get(name=domain_name)
        except Domain.DoesNotExist:
            raise CommandError(f'Domain "{domain_name}" does not exist')

        self.stdout.write(f'Applying modern stylesheet to domain: {domain.name}')

        # Define modern stylesheet content
        stylesheet_content = """
/* Modern Theme - Nature Inspired Design */

:root {
    --color-forest: #1b4d3e;
    --color-forest-light: #2d5016;
    --color-ocean: #0066cc;
    --color-ocean-light: #4a90e2;
    --color-earth: #8b6f47;
    --color-terracotta: #d97e6e;
}

/* Custom color overrides and domain-specific styling can go here */
"""

        stylesheet, created = Stylesheet.objects.get_or_create(
            domain=domain,
            name='Modern Theme',
            defaults={
                'description': 'Modern responsive stylesheet with nature-inspired bold colors (forest, ocean, earth)',
                'is_active': True,
            }
        )

        # Save the CSS file
        if created or not stylesheet.css_file:
            filename = f'modern-theme-{domain.name}.css'
            stylesheet.css_file.save(
                filename,
                ContentFile(stylesheet_content.encode('utf-8'))
            )
            stylesheet.save()
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created stylesheet: {stylesheet.name}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⊘ Stylesheet already exists: {stylesheet.name}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\nStylesheet applied successfully to {domain.name}')
        )
        self.stdout.write(
            self.style.WARNING(
                '\nNote: The main CSS is in static/css/modern-base.css\n'
                'This stylesheet can contain domain-specific overrides and customizations.'
            )
        )
