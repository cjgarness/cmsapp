from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from cmsapp.templates.models import PageTemplate, Stylesheet


class Page(models.Model):
    """CMS Page model with customizable layout and template support."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    template = models.ForeignKey(
        PageTemplate, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='pages'
    )
    stylesheets = models.ManyToManyField(
        Stylesheet, 
        blank=True, 
        related_name='pages'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    featured_image = models.ImageField(upload_to='pages/featured/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    author = models.CharField(max_length=100, default='Admin')
    is_homepage = models.BooleanField(default=False)
    show_in_menu = models.BooleanField(default=True)
    show_in_navbar = models.BooleanField(default=False)
    show_in_page_list = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Pages'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        if self.is_homepage:
            return '/'
        return f'/{self.slug}/'


class PageBlock(models.Model):
    """Reusable content blocks for pages."""
    
    BLOCK_TYPES = [
        ('text', 'Text Block'),
        ('image', 'Image Block'),
        ('gallery', 'Gallery Block'),
        ('video', 'Video Block'),
        ('code', 'Code Block'),
        ('custom', 'Custom HTML'),
    ]
    
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='blocks')
    title = models.CharField(max_length=100, blank=True)
    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES, default='text')
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Page Blocks'
    
    def __str__(self):
        return f"{self.page.title} - {self.title}"


class PageImage(models.Model):
    """Image assets for pages with metadata."""
    
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pages/images/')
    alt_text = models.CharField(max_length=255)
    caption = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Page Images'
    
    def __str__(self):
        return f"{self.page.title} - {self.alt_text}"
