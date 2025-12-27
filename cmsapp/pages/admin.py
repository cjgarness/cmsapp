from django.contrib import admin
from .models import Page, PageBlock, PageImage


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'is_homepage', 'show_in_menu', 'show_in_navbar', 'show_in_page_list', 'created_at')
    list_filter = ('status', 'is_homepage', 'show_in_menu', 'show_in_navbar', 'show_in_page_list', 'created_at')
    search_fields = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'featured_image')
        }),
        ('Content', {
            'fields': ('content', 'template', 'stylesheets')
        }),
        ('Publishing', {
            'fields': ('status', 'is_homepage', 'show_in_menu', 'show_in_navbar', 'show_in_page_list', 'author', 'created_at', 'updated_at', 'published_at')
        }),
    )


@admin.register(PageBlock)
class PageBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'page', 'block_type', 'order')
    list_filter = ('block_type', 'page')
    search_fields = ('title', 'page__title')


@admin.register(PageImage)
class PageImageAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'page', 'uploaded_at')
    list_filter = ('uploaded_at', 'page')
    search_fields = ('alt_text', 'page__title')
