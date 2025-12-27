from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Page


class PageListView(ListView):
    model = Page
    template_name = 'pages/page_list.html'
    context_object_name = 'pages'
    paginate_by = 10
    
    def get_queryset(self):
        return Page.objects.filter(status='published', show_in_menu=True, show_in_page_list=True).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_pages'] = Page.objects.filter(show_in_navbar=True, status='published')
        return context


class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page_detail.html'
    context_object_name = 'page'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Page.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        context['blocks'] = page.blocks.all().order_by('order')
        context['stylesheets'] = page.stylesheets.all()
        context['images'] = page.images.all()
        context['navbar_pages'] = Page.objects.filter(show_in_navbar=True, status='published')
        return context


def homepage_view(request):
    """Display the homepage."""
    homepage = get_object_or_404(Page, is_homepage=True, status='published')
    context = {
        'page': homepage,
        'blocks': homepage.blocks.all().order_by('order'),
        'stylesheets': homepage.stylesheets.all(),
        'images': homepage.images.all(),
        'navbar_pages': Page.objects.filter(show_in_navbar=True, status='published')
    }
    if homepage.template:
        return render(request, homepage.template.template_file.name, context)
    return render(request, 'pages/page_detail.html', context)
