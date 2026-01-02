"""
Management command to set up modern templates for a specific domain.
Usage: python manage.py setup_modern_templates --domain altuspath.com
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from cmsapp.templates.models import PageTemplate
from cmsapp.domains.models import Domain
from cmsapp.domains.utils import get_domain_or_raise


class Command(BaseCommand):
    help = 'Set up modern responsive templates for a domain'

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

        self.stdout.write(f'Setting up modern templates for domain: {domain.name}')

        templates_to_create = [
            {
                'name': 'Modern Base',
                'template_name': 'modern/base.html',
                'description': 'Base template with responsive navigation and footer',
                'is_default': False,
            },
            {
                'name': 'Modern Page Detail',
                'template_name': 'modern/page_detail.html',
                'description': 'Template for individual page display with hero section',
                'is_default': True,
            },
            {
                'name': 'Modern Page List',
                'template_name': 'modern/page_list.html',
                'description': 'Template for displaying pages in a grid layout',
                'is_default': False,
            },
            {
                'name': 'Modern Homepage',
                'template_name': 'modern/homepage.html',
                'description': 'Template for homepage with featured sections',
                'is_default': False,
            },
        ]

        created_count = 0
        for template_data in templates_to_create:
            template, created = PageTemplate.objects.get_or_create(
                domain=domain,
                template_name=template_data['template_name'],
                defaults={
                    'name': template_data['name'],
                    'description': template_data['description'],
                    'is_default': template_data['is_default'],
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {template.name}')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'⊘ Already exists: {template.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nCompleted! Created {created_count} templates for {domain.name}')
        )
