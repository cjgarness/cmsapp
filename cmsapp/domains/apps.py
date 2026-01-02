from django.apps import AppConfig


class DomainsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cmsapp.domains'
    verbose_name = 'Domain Management'
    
    def ready(self):
        """Import signals when app is ready."""
        import cmsapp.domains.signals
