from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from .models import ContactInquiry, ContactConfiguration, InquiryType


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'inquiry_type_badge',
        'message_preview',
        'status_badge',
        'created_at',
    ]
    list_filter = ['domain', 'status', 'inquiry_type', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = [
        'created_at',
        'updated_at',
        'read_at',
        'responded_at',
        'formatted_message',
    ]
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('domain', 'inquiry_type', 'formatted_message')
        }),
        ('Status & Notes', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'read_at', 'responded_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_read', 'mark_as_responded', 'mark_as_closed']
    
    def inquiry_type_badge(self, obj):
        # Handle None inquiry_type
        if not obj.inquiry_type:
            return format_html(
                '<span style="background-color: #95a5a6; color: white; padding: 3px 8px; border-radius: 3px;">Unknown</span>'
            )
        
        # Use a hash of the inquiry type slug to generate a consistent color
        color_map = {
            0: '#3498db',
            1: '#2ecc71',
            2: '#e74c3c',
            3: '#f39c12',
            4: '#9b59b6',
            5: '#95a5a6',
        }
        color_index = hash(obj.inquiry_type.slug) % 6
        color = color_map.get(color_index, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.inquiry_type.label
        )
    inquiry_type_badge.short_description = 'Type'
    
    def status_badge(self, obj):
        colors = {
            'new': '#e74c3c',
            'read': '#f39c12',
            'responded': '#2ecc71',
            'closed': '#95a5a6',
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def message_preview(self, obj):
        content = obj.message or ''
        return (content[:50] + '...') if len(content) > 50 else content
    message_preview.short_description = 'Message'
    
    def formatted_message(self, obj):
        return format_html('<p style="white-space: pre-wrap;">{}</p>', obj.message)
    formatted_message.short_description = 'Message'
    
    def mark_as_read(self, request, queryset):
        updated = 0
        for inquiry in queryset:
            inquiry.mark_as_read()
            updated += 1
        self.message_user(request, f'{updated} inquiries marked as read.')
    mark_as_read.short_description = 'Mark selected as Read'
    
    def mark_as_responded(self, request, queryset):
        updated = queryset.update(status='responded', responded_at=timezone.now())
        self.message_user(request, f'{updated} inquiries marked as Responded.')
    mark_as_responded.short_description = 'Mark selected as Responded'
    
    def mark_as_closed(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} inquiries marked as Closed.')
    mark_as_closed.short_description = 'Mark selected as Closed'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Mark new inquiries as read when viewing
        new_inquiries = qs.filter(status='new')
        for inquiry in new_inquiries:
            inquiry.mark_as_read()
        return qs


@admin.register(ContactConfiguration)
class ContactConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Email Notifications', {
            'fields': ('admin_email', 'admin_name', 'send_confirmation_email')
        }),
        ('SMS Notifications', {
            'fields': (
                'enable_sms_notifications',
                'sms_phone_number',
                'sms_api_key'
            ),
            'classes': ('collapse',),
            'description': 'Optional: Configure SMS notifications using Twilio'
        }),
        ('General Settings', {
            'fields': ('enable_contact_form', 'auto_response_enabled')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        # Only allow one configuration object
        return not ContactConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(InquiryType)
class InquiryTypeAdmin(admin.ModelAdmin):
    list_display = ['label', 'domain', 'slug', 'order', 'is_active', 'created_at']
    list_filter = ['domain', 'is_active', 'created_at']
    search_fields = ['label', 'slug', 'domain__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('domain', 'label', 'slug')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Filter inquiry types by domain if user has domain restrictions."""
        qs = super().get_queryset(request)
        # If using multi-domain middleware, filter by user's domains
        if hasattr(request, 'domain'):
            qs = qs.filter(domain=request.domain)
        return qs
