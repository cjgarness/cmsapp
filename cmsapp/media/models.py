from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os


class MediaFolder(models.Model):
    """Organize media files into folders."""
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='subfolders'
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Media Folders'
    
    def __str__(self):
        if self.parent:
            return f"{self.parent} / {self.name}"
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_path(self):
        """Get the full folder path."""
        if self.parent:
            return f"{self.parent.get_path()}/{self.slug}"
        return self.slug


class MediaFile(models.Model):
    """Uploaded media files with metadata."""
    
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='media_library/%Y/%m/')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, default='other')
    folder = models.ForeignKey(
        MediaFolder, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='files'
    )
    
    # File metadata
    file_size = models.PositiveIntegerField(null=True, blank=True, help_text='File size in bytes')
    file_extension = models.CharField(max_length=10, blank=True)
    mime_type = models.CharField(max_length=100, blank=True)
    
    # Image-specific fields
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True, help_text='Alternative text for images')
    
    # Metadata
    uploaded_by = models.CharField(max_length=100, default='Admin')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Usage tracking
    usage_count = models.PositiveIntegerField(default=0, help_text='Number of times this file is used')
    last_used = models.DateTimeField(null=True, blank=True)
    
    # Tags for organization
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags')
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = 'Media Files'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Extract file metadata if file exists
        if self.file:
            self.file_size = self.file.size
            self.file_extension = os.path.splitext(self.file.name)[1].lower().replace('.', '')
            
            # Auto-detect media type based on extension
            if not self.media_type or self.media_type == 'other':
                self.media_type = self._detect_media_type()
            
            # Get image dimensions for image files
            if self.media_type == 'image' and not self.width:
                try:
                    from PIL import Image
                    image = Image.open(self.file)
                    self.width, self.height = image.size
                except Exception:
                    pass
        
        super().save(*args, **kwargs)
    
    def _detect_media_type(self):
        """Auto-detect media type from file extension."""
        image_exts = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp', 'ico']
        video_exts = ['mp4', 'webm', 'ogg', 'mov', 'avi', 'wmv', 'flv']
        audio_exts = ['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a']
        doc_exts = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'csv']
        
        ext = self.file_extension.lower()
        if ext in image_exts:
            return 'image'
        elif ext in video_exts:
            return 'video'
        elif ext in audio_exts:
            return 'audio'
        elif ext in doc_exts:
            return 'document'
        return 'other'
    
    def get_absolute_url(self):
        """Get the URL to access this file."""
        return self.file.url if self.file else ''
    
    def get_file_size_display(self):
        """Human-readable file size."""
        if not self.file_size:
            return 'Unknown'
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
    
    def increment_usage(self):
        """Track usage of this media file."""
        self.usage_count += 1
        self.last_used = timezone.now()
        self.save(update_fields=['usage_count', 'last_used'])


class MediaGallery(models.Model):
    """Collection of media files that can be embedded in pages."""
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    files = models.ManyToManyField(MediaFile, related_name='galleries', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Media Galleries'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
