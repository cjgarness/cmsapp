from django.db import models


class PageTemplate(models.Model):
    """Customizable page layout templates."""
    
    LAYOUT_CHOICES = [
        ('single-column', 'Single Column'),
        ('two-column', 'Two Column'),
        ('three-column', 'Three Column'),
        ('hero', 'Hero Layout'),
        ('masonry', 'Masonry Layout'),
        ('custom', 'Custom Layout'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    layout_type = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='single-column')
    template_file = models.FileField(
        upload_to='templates/',
        help_text='Django template file with .html extension'
    )
    thumbnail = models.ImageField(upload_to='templates/thumbnails/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Page Templates'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Stylesheet(models.Model):
    """CSS stylesheets for customization."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    css_file = models.FileField(
        upload_to='stylesheets/',
        help_text='CSS file'
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Stylesheets'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class LayoutComponent(models.Model):
    """Reusable layout components for templates."""
    
    COMPONENT_TYPES = [
        ('header', 'Header'),
        ('sidebar', 'Sidebar'),
        ('footer', 'Footer'),
        ('section', 'Section'),
        ('widget', 'Widget'),
    ]
    
    name = models.CharField(max_length=100)
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    template = models.ForeignKey(PageTemplate, on_delete=models.CASCADE, related_name='components')
    html_content = models.TextField(help_text='HTML markup for the component')
    css_class = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Layout Components'
        unique_together = ('template', 'component_type')
    
    def __str__(self):
        return f"{self.template.name} - {self.component_type}"
