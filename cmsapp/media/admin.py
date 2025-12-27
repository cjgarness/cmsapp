from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import MediaFolder, MediaFile, MediaGallery


@admin.register(MediaFolder)
class MediaFolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'file_count', 'created_at')
    list_filter = ('created_at', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(files_count=Count('files'))
    
    def file_count(self, obj):
        return obj.files_count if hasattr(obj, 'files_count') else obj.files.count()
    file_count.short_description = 'Files'
    file_count.admin_order_field = 'files_count'


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = (
        'thumbnail_preview', 'title', 'media_type', 'folder', 
        'file_size_display', 'usage_count', 'uploaded_at'
    )
    list_filter = ('media_type', 'folder', 'uploaded_at')
    search_fields = ('title', 'description', 'tags', 'alt_text')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = (
        'file_preview', 'uploaded_at', 'updated_at', 'file_size', 
        'file_extension', 'width', 'height', 'last_used'
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'file', 'media_type', 'folder')
        }),
        ('File Details', {
            'fields': ('file_size', 'file_extension', 'mime_type', 'width', 'height')
        }),
        ('Media Attributes', {
            'fields': ('alt_text', 'tags')
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'uploaded_at', 'updated_at', 'usage_count', 'last_used')
        }),
        ('Preview', {
            'fields': ('file_preview',),
            'classes': ('collapse',)
        }),
    )
    
    def thumbnail_preview(self, obj):
        if obj.media_type == 'image' and obj.file:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; object-fit: cover;" />',
                obj.file.url
            )
        elif obj.media_type == 'video':
            return format_html('<span style="font-size: 20px;">🎬</span>')
        elif obj.media_type == 'audio':
            return format_html('<span style="font-size: 20px;">🎵</span>')
        elif obj.media_type == 'document':
            return format_html('<span style="font-size: 20px;">📄</span>')
        return format_html('<span style="font-size: 20px;">📁</span>')
    thumbnail_preview.short_description = 'Preview'
    
    def file_preview(self, obj):
        if obj.media_type == 'image' and obj.file:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 400px;" /><br/><br/>'
                '<strong>URL:</strong> <input type="text" value="{}" readonly style="width: 100%;" />',
                obj.file.url,
                obj.file.url
            )
        elif obj.media_type == 'video' and obj.file:
            return format_html(
                '<video controls style="max-width: 400px;"><source src="{}"></video><br/><br/>'
                '<strong>URL:</strong> <input type="text" value="{}" readonly style="width: 100%;" />',
                obj.file.url,
                obj.file.url
            )
        elif obj.media_type == 'audio' and obj.file:
            return format_html(
                '<audio controls><source src="{}"></audio><br/><br/>'
                '<strong>URL:</strong> <input type="text" value="{}" readonly style="width: 100%;" />',
                obj.file.url,
                obj.file.url
            )
        elif obj.file:
            return format_html(
                '<strong>URL:</strong> <input type="text" value="{}" readonly style="width: 100%;" /><br/><br/>'
                '<a href="{}" target="_blank" class="button">Download File</a>',
                obj.file.url,
                obj.file.url
            )
        return 'No file uploaded'
    file_preview.short_description = 'File Preview & URL'
    
    def file_size_display(self, obj):
        return obj.get_file_size_display()
    file_size_display.short_description = 'Size'
    file_size_display.admin_order_field = 'file_size'


@admin.register(MediaGallery)
class MediaGalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'file_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('files',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Media Files', {
            'fields': ('files',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def file_count(self, obj):
        return obj.files.count()
    file_count.short_description = 'Files'
