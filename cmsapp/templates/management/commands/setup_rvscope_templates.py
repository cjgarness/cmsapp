"""
Management command to set up RVScope templates for a specific domain.
Usage: python manage.py setup_rvscope_templates --domain rvscope.com
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from cmsapp.templates.models import PageTemplate
from cmsapp.domains.models import Domain
import os


class Command(BaseCommand):
    help = 'Set up RVScope Bootstrap templates for a domain'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            default='rvscope.com',
            help='Domain name (default: rvscope.com)',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        domain_name = options['domain']
        
        try:
            domain = Domain.objects.get(name=domain_name)
        except Domain.DoesNotExist:
            raise CommandError(f'Domain "{domain_name}" does not exist')

        self.stdout.write(f'Setting up RVScope templates for domain: {domain.name}')

        templates_to_create = [
            {
                'name': 'RVScope Page Detail',
                'description': 'Bootstrap template for individual page display with sidebar',
                'layout_type': 'hero',
                'template_path': 'rvscope/page_detail.html',
            },
            {
                'name': 'RVScope Page List',
                'description': 'Bootstrap template for displaying pages in a card grid',
                'layout_type': 'masonry',
                'template_path': 'rvscope/page_list.html',
            },
            {
                'name': 'RVScope Homepage',
                'description': 'Bootstrap template for homepage with hero section and featured content',
                'layout_type': 'hero',
                'template_path': 'rvscope/homepage.html',
            },
            {
                'name': 'RVScope Contact',
                'description': 'Bootstrap template for contact form with multi-column layout',
                'layout_type': 'single-column',
                'template_path': 'rvscope/contact.html',
            },
        ]

        created_count = 0
        for template_data in templates_to_create:
            # Read the template file - navigate from cmsapp/templates/management/commands to project root
            # __file__ = .../cmsapp/templates/management/commands/setup_rvscope_templates.py
            # We need to go up 5 levels to get to project root, then into templates/
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
            template_file_path = os.path.join(
                project_root,
                'templates',
                template_data['template_path']
            )
            
            if not os.path.exists(template_file_path):
                self.stdout.write(
                    self.style.WARNING(f'⊘ Template file not found: {template_file_path}')
                )
                continue
            
            # Read template content for verification
            with open(template_file_path, 'r') as f:
                template_content = f.read()
            
            template, created = PageTemplate.objects.get_or_create(
                domain=domain,
                name=template_data['name'],
                defaults={
                    'description': template_data['description'],
                    'layout_type': template_data['layout_type'],
                    'template_name': template_data['template_path'],
                    'template_file': '',  # Not used but required by database
                    'is_active': True,
                }
            )

            if created:
                # Note: File is not copied to media folder due to permissions,
                # but template reference is stored in the database
                # The template files live in the templates directory and are referenced by name
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {template.name} (file: {template_data["template_path"]})')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'⊘ Already exists: {template.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nCompleted! Created {created_count} templates for {domain.name}')
        )
        self.stdout.write(
            self.style.SUCCESS(
                '\nRVScope templates are now available in the database.\n'
                'Template files are located in: templates/rvscope/\n'
                'These templates use Bootstrap 5 with professional dark headers and card layouts.'
            )
        )
