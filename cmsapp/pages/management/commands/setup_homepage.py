"""
Management command to set up homepage for a domain.
Usage: python manage.py setup_homepage --domain altuspath.com
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from cmsapp.pages.models import Page
from cmsapp.templates.models import PageTemplate
from cmsapp.domains.models import Domain


class Command(BaseCommand):
    help = 'Set up a homepage page for a domain'

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

        self.stdout.write(f'Setting up homepage for domain: {domain.name}')

        # Check if homepage already exists
        try:
            homepage = Page.objects.get(is_homepage=True, domain=domain)
            self.stdout.write(
                self.style.WARNING(f'⊘ Homepage already exists: {homepage.title}')
            )
            return
        except Page.DoesNotExist:
            pass

        # Get the Modern Homepage template
        try:
            template = PageTemplate.objects.get(
                domain=domain,
                name='Modern Homepage'
            )
        except PageTemplate.DoesNotExist:
            raise CommandError(
                f'Modern Homepage template not found for domain {domain_name}. '
                'Run setup_modern_templates first.'
            )

        # Create homepage
        homepage = Page.objects.create(
            domain=domain,
            title='Welcome to AltusPath',
            slug='home',
            description='Welcome to AltusPath - Building modern web experiences',
            content='<h2>Welcome!</h2><p>Edit this content in the admin dashboard.</p>',
            template=template,
            status='published',
            is_homepage=True,
            show_in_menu=False,
            show_in_navbar=False,
            show_in_page_list=False,
            author='System'
        )

        self.stdout.write(
            self.style.SUCCESS(f'✓ Created homepage: {homepage.title}')
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'\nHomepage is ready! Access it at: http://{domain.name}/'
            )
        )
