from django.contrib import admin
from .models import Page, PageBlock, PageImage
from cmsapp.domains.utils import filter_queryset_by_domain, get_user_domains


class PageBlockInline(admin.TabularInline):
    """Inline admin for editing page blocks directly within the page admin."""
    model = PageBlock
    extra = 0
    fields = ('title', 'block_type', 'content', 'order')
    ordering = ('order',)
    
    def has_add_permission(self, request, obj=None):
        """Allow adding new blocks."""
        return True


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'domain', 'status', 'is_homepage', 'show_in_menu', 'created_at')
    list_filter = ('domain', 'status', 'is_homepage', 'show_in_menu', 'show_in_navbar', 'show_in_page_list', 'created_at')
    search_fields = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    inlines = [PageBlockInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('domain', 'title', 'slug', 'description', 'featured_image')
        }),
        ('Content', {
            'fields': ('content', 'template', 'stylesheets')
        }),
        ('Publishing', {
            'fields': ('status', 'is_homepage', 'show_in_menu', 'show_in_navbar', 'show_in_page_list', 'author', 'created_at', 'updated_at', 'published_at')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return filter_queryset_by_domain(qs, request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'domain' and not request.user.is_superuser:
            kwargs["queryset"] = get_user_domains(request.user)
        if db_field.name == 'template':
            kwargs["queryset"] = filter_queryset_by_domain(
                db_field.remote_field.model.objects.all(),
                request.user
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'stylesheets':
            kwargs["queryset"] = filter_queryset_by_domain(
                db_field.remote_field.model.objects.all(),
                request.user
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)


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
