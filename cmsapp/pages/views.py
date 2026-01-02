from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Page


class PageListView(ListView):
    model = Page
    context_object_name = 'pages'
    paginate_by = 10
    
    def get_template_names(self):
        """Return domain-specific template based on current domain."""
        domain = getattr(self.request, 'domain', None)
        
        # Map domains to their template directories
        domain_templates = {
            'altuspath.com': ['modern/page_list.html', 'pages/page_list.html'],
            'rvscope.com': ['rvscope/page_list.html', 'pages/page_list.html'],
        }
        
        if domain and domain.name in domain_templates:
            return domain_templates[domain.name]
        
        # Default fallback
        return ['modern/page_list.html', 'pages/page_list.html']
    
    def get_queryset(self):
        domain = getattr(self.request, 'domain', None)
        qs = Page.objects.filter(status='published', show_in_menu=True, show_in_page_list=True)
        if domain:
            qs = qs.filter(domain=domain)
        return qs.order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domain = getattr(self.request, 'domain', None)
        navbar_qs = Page.objects.filter(show_in_navbar=True, status='published')
        if domain:
            navbar_qs = navbar_qs.filter(domain=domain)
        context['navbar_pages'] = navbar_qs
        return context


class PageDetailView(DetailView):
    model = Page
    context_object_name = 'page'
    slug_field = 'slug'
    
    def get_template_names(self):
        """Return domain-specific template based on current domain."""
        page = self.get_object()
        domain = getattr(self.request, 'domain', None)
        
        # If page has a template assigned, use it first
        if page.template and page.template.template_name:
            return [page.template.template_name]
        
        # Map domains to their template directories
        domain_templates = {
            'altuspath.com': ['modern/page_detail.html', 'pages/page_detail.html'],
            'rvscope.com': ['rvscope/page_detail.html', 'pages/page_detail.html'],
        }
        
        if domain and domain.name in domain_templates:
            return domain_templates[domain.name]
        
        # Default fallback
        return ['modern/page_detail.html', 'pages/page_detail.html']
    
    def get_queryset(self):
        domain = getattr(self.request, 'domain', None)
        qs = Page.objects.filter(status='published')
        if domain:
            qs = qs.filter(domain=domain)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        domain = getattr(self.request, 'domain', None)
        navbar_qs = Page.objects.filter(show_in_navbar=True, status='published')
        if domain:
            navbar_qs = navbar_qs.filter(domain=domain)
        context['blocks'] = page.blocks.all().order_by('order')
        context['stylesheets'] = page.stylesheets.all()
        context['images'] = page.images.all()
        context['navbar_pages'] = navbar_qs
        return context


def homepage_view(request):
    """Display the homepage."""
    domain = getattr(request, 'domain', None)
    
    # Filter by domain if available
    try:
        if domain:
            homepage = get_object_or_404(Page, is_homepage=True, status='published', domain=domain)
        else:
            homepage = get_object_or_404(Page, is_homepage=True, status='published')
    except:
        homepage = get_object_or_404(Page, is_homepage=True, status='published')
    
    navbar_qs = Page.objects.filter(show_in_navbar=True, status='published')
    if domain:
        navbar_qs = navbar_qs.filter(domain=domain)
    
    context = {
        'page': homepage,
        'blocks': homepage.blocks.all().order_by('order'),
        'stylesheets': homepage.stylesheets.all(),
        'images': homepage.images.all(),
        'navbar_pages': navbar_qs
    }
    
    # Use template_name if available
    if homepage.template and homepage.template.template_name:
        return render(request, homepage.template.template_name, context)
    
    # Fall back to domain-specific template
    if domain and domain.name == 'rvscope.com':
        return render(request, 'rvscope/homepage.html', context)
    
    # Default to modern template
    return render(request, 'modern/homepage.html', context)
