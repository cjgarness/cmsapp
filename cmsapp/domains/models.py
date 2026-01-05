from django.db import models
from django.contrib.auth.models import User


class Domain(models.Model):
    """Represents a separate website with independent content and configuration."""
    
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Domain name (e.g., example.com)"
    )
    title = models.CharField(
        max_length=200,
        help_text="Display name for this domain"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of this domain/website"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Enable/disable this domain"
    )
    
    # Branding
    logo = models.ImageField(
        upload_to='domain-logos/',
        blank=True,
        null=True
    )
    favicon = models.ImageField(
        upload_to='domain-favicons/',
        blank=True,
        null=True
    )
    
    # Contact info
    contact_email = models.EmailField(
        blank=True,
        help_text="Primary contact email for this domain"
    )
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Contact phone number"
    )
    contact_address = models.TextField(
        blank=True,
        help_text="Physical address"
    )
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Domains'
        indexes = [
            models.Index(fields=['is_active', 'name']),
        ]
    
    def __str__(self):
        status = "✓" if self.is_active else "✗"
        return f"{status} {self.name} - {self.title}"


class DomainPermission(models.Model):
    """Control which users can manage which domains."""
    
    ROLE_CHOICES = [
        ('viewer', 'Viewer (Read-only)'),
        ('editor', 'Editor (Can create/edit)'),
        ('admin', 'Admin (Full control)'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='domain_permissions'
    )
    domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE,
        related_name='user_permissions'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='editor'
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'domain')
        verbose_name_plural = 'Domain Permissions'
        ordering = ['domain', 'user']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['domain', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.domain.name} ({self.role})"
    
    def has_edit_permission(self):
        """Check if user has edit permission."""
        return self.role in ['editor', 'admin'] and self.is_active
    
    def has_admin_permission(self):
        """Check if user has admin permission."""
        return self.role == 'admin' and self.is_active


class DomainSetting(models.Model):
    """Store domain-specific settings."""
    
    domain = models.OneToOneField(
        Domain,
        on_delete=models.CASCADE,
        related_name='settings'
    )
    
    # SEO
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Default meta description for pages"
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Default meta keywords (comma-separated)"
    )
    
    # Feature flags
    enable_contact_form = models.BooleanField(default=True)
    enable_comments = models.BooleanField(default=False)
    enable_search = models.BooleanField(default=True)
    
    # Customization
    custom_css = models.TextField(
        blank=True,
        help_text="Custom CSS for this domain"
    )
    custom_js = models.TextField(
        blank=True,
        help_text="Custom JavaScript for this domain"
    )

    # Navigation
    show_pages_link = models.BooleanField(
        default=True,
        help_text="Show the Pages link in the navigation bar"
    )
    
    # Visual Customization
    show_background_watermark = models.BooleanField(
        default=True,
        help_text="Show background watermark image on all pages"
    )
    
    google_analytics_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Google Analytics tracking ID (e.g., UA-XXXXXXXXX-X or G-XXXXXXXXXX)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Domain Setting'
        verbose_name_plural = 'Domain Settings'
    
    def __str__(self):
        return f"Settings for {self.domain.name}"
