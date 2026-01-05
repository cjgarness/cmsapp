"""
URL configuration for cmsapp project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin site
admin.site.site_header = "CMS Administration"
admin.site.site_title = "CMS Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('contact/', include('cmsapp.contact.urls')),
    path('', include('cmsapp.pages.urls')),
    path('api/', include('cmsapp.core.urls')),
    path('media/', include('cmsapp.media.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
