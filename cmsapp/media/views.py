from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import MediaFile, MediaFolder, MediaGallery


@method_decorator(staff_member_required, name='dispatch')
class MediaLibraryView(ListView):
    """Browse the media library."""
    model = MediaFile
    template_name = 'media/media_library.html'
    context_object_name = 'media_files'
    paginate_by = 24
    
    def get_queryset(self):
        qs = MediaFile.objects.all()
        
        # Filter by current domain
        current_domain = getattr(self.request, 'domain', None)
        if current_domain:
            qs = qs.filter(domain=current_domain)
        
        # Filter by media type
        media_type = self.request.GET.get('type')
        if media_type:
            qs = qs.filter(media_type=media_type)
        
        # Filter by folder
        folder_id = self.request.GET.get('folder')
        if folder_id:
            qs = qs.filter(folder_id=folder_id)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(tags__icontains=search)
        
        return qs.order_by('-uploaded_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_domain = getattr(self.request, 'domain', None)
        
        # Filter folders by current domain
        if current_domain:
            context['folders'] = MediaFolder.objects.filter(domain=current_domain)
        else:
            context['folders'] = MediaFolder.objects.all()
        
        context['current_folder'] = self.request.GET.get('folder')
        context['current_type'] = self.request.GET.get('type')
        context['search_query'] = self.request.GET.get('search', '')
        return context


@method_decorator(staff_member_required, name='dispatch')
class MediaFileDetailView(DetailView):
    """View details of a media file."""
    model = MediaFile
    template_name = 'media/media_detail.html'
    context_object_name = 'media_file'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get other files in the same folder
        if self.object.folder:
            context['related_files'] = MediaFile.objects.filter(
                folder=self.object.folder
            ).exclude(id=self.object.id)[:6]
        return context
