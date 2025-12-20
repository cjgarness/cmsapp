from django.contrib import admin
from .models import PageTemplate, Stylesheet, LayoutComponent


@admin.register(PageTemplate)
class PageTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'layout_type', 'is_active', 'created_at')
    list_filter = ('layout_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Stylesheet)
class StylesheetAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LayoutComponent)
class LayoutComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'template', 'component_type', 'created_at')
    list_filter = ('component_type', 'template', 'created_at')
    search_fields = ('name', 'template__name')
    readonly_fields = ('created_at', 'updated_at')
