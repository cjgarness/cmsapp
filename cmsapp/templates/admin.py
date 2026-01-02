from django.contrib import admin
from .models import PageTemplate, Stylesheet, LayoutComponent
from cmsapp.domains.utils import filter_queryset_by_domain, get_user_domains


@admin.register(PageTemplate)
class PageTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'layout_type', 'is_active', 'created_at')
    list_filter = ('domain', 'layout_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return filter_queryset_by_domain(qs, request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'domain' and not request.user.is_superuser:
            kwargs["queryset"] = get_user_domains(request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Stylesheet)
class StylesheetAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'is_active', 'order', 'created_at')
    list_filter = ('domain', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return filter_queryset_by_domain(qs, request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'domain' and not request.user.is_superuser:
            kwargs["queryset"] = get_user_domains(request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(LayoutComponent)
class LayoutComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'template', 'component_type', 'created_at')
    list_filter = ('component_type', 'template', 'created_at')
    search_fields = ('name', 'template__name')
    readonly_fields = ('created_at', 'updated_at')
