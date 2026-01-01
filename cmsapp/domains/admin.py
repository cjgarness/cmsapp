from django.contrib import admin
from django.utils.html import format_html
from .models import Domain, DomainPermission, DomainSetting


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'title',
        'status_badge',
        'user_count',
        'created_at',
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Domain Information', {
            'fields': ('name', 'title', 'description', 'is_active')
        }),
        ('Branding', {
            'fields': ('logo', 'favicon'),
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'contact_address'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def status_badge(self, obj):
        color = '#2ecc71' if obj.is_active else '#e74c3c'
        status = 'Active' if obj.is_active else 'Inactive'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            status
        )
    status_badge.short_description = 'Status'
    
    def user_count(self, obj):
        count = obj.user_permissions.filter(is_active=True).count()
        return count
    user_count.short_description = 'Active Users'


@admin.register(DomainPermission)
class DomainPermissionAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'domain',
        'role_badge',
        'is_active',
        'created_at',
    ]
    list_filter = ['domain', 'role', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'domain__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Permission Details', {
            'fields': ('user', 'domain', 'role', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def role_badge(self, obj):
        colors = {
            'viewer': '#3498db',
            'editor': '#f39c12',
            'admin': '#e74c3c',
        }
        color = colors.get(obj.role, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_role_display()
        )
    role_badge.short_description = 'Role'


@admin.register(DomainSetting)
class DomainSettingAdmin(admin.ModelAdmin):
    list_display = ['domain', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Domain', {
            'fields': ('domain',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
        }),
        ('Features', {
            'fields': (
                'enable_contact_form',
                'enable_comments',
                'enable_search',
            ),
        }),
        ('Customization', {
            'fields': (
                'custom_css',
                'custom_js',
            ),
        }),
        ('Analytics', {
            'fields': ('google_analytics_id',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def has_add_permission(self, request):
        # Can only add settings if there's a domain without settings
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False
