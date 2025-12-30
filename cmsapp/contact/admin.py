from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q
from .models import ContactInquiry, ContactConfiguration


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'inquiry_type_badge',
        'subject_short',
        'status_badge',
        'created_at',
    ]
    list_filter = ['status', 'inquiry_type', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = [
        'created_at',
        'updated_at',
        'read_at',
        'responded_at',
        'formatted_message',
    ]
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry_type', 'subject', 'formatted_message')
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
        colors = {
            'question': '#3498db',
            'service': '#2ecc71',
            'support': '#e74c3c',
            'feedback': '#f39c12',
            'partnership': '#9b59b6',
            'other': '#95a5a6',
        }
        color = colors.get(obj.inquiry_type, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_inquiry_type_display()
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
    
    def subject_short(self, obj):
        return obj.subject[:50] + '...' if len(obj.subject) > 50 else obj.subject
    subject_short.short_description = 'Subject'
    
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


# Import timezone at the top
from django.utils import timezone
