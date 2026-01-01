# Multi-Domain CMS Guide

The CMS now supports multiple independent websites within a single instance. Each domain has its own content, templates, stylesheets, and media library. Users can be granted different permission levels for each domain.

## Architecture Overview

### Core Models

1. **Domain** - Represents a separate website
   - Domain name (e.g., example.com)
   - Title and description
   - Branding (logo, favicon)
   - Contact information
   - Active/inactive status

2. **DomainPermission** - Controls user access to domains
   - Links users to domains
   - Three permission levels: Viewer, Editor, Admin
   - Independent for each domain

3. **DomainSetting** - Domain-specific configuration
   - SEO settings (meta description, keywords)
   - Feature toggles (contact form, comments, search)
   - Custom CSS/JavaScript
   - Google Analytics tracking

### Content Models (Domain-Aware)

The following models are now domain-specific:
- **Page** - Pages belong to a specific domain
- **PageTemplate** - Templates are domain-specific
- **Stylesheet** - Stylesheets are domain-specific
- **MediaFolder** - Media folders are domain-specific
- **MediaFile** - Media files are domain-specific

## Setup Instructions

### 1. Create Migrations

After the code changes, create and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Your First Domain

Access the Django admin panel at `/admin/` and navigate to **Domain Management > Domains**.

Click "Add Domain" and fill in:
- **Name**: example.com (the actual domain)
- **Title**: My Website (display name)
- **Description**: Optional description
- **Contact Email/Phone/Address**: Optional contact information
- **Logo/Favicon**: Optional branding images

### 3. Configure Domain Settings

1. Go to **Domain Management > Domain Settings**
2. Click "Add Domain Setting"
3. Select your domain and configure:
   - SEO metadata
   - Feature flags (enable/disable contact form, comments, etc.)
   - Custom CSS/JavaScript
   - Google Analytics ID

### 4. Create Content for the Domain

Once a domain exists, you can create:
- **Pages** (Pages > Pages) - automatically scoped to the domain
- **Templates** (Templates > Page Templates) - domain-specific templates
- **Stylesheets** (Templates > Stylesheets) - domain-specific CSS
- **Media** (Media > Media Folders/Files) - domain-organized library

### 5. Grant User Permissions

1. Go to **Domain Management > Domain Permissions**
2. Click "Add Domain Permission"
3. Select:
   - **User** - The user to grant permission to
   - **Domain** - Which domain they can access
   - **Role** - Their permission level:
     - **Viewer**: Read-only access
     - **Editor**: Can create and edit content
     - **Admin**: Full control including settings

## Permission Levels Explained

### Viewer (Read-only)
- Can view content on the domain
- Cannot create or modify anything
- Cannot access settings

### Editor
- Can create and edit pages, templates, media
- Cannot modify domain settings
- Cannot manage user permissions

### Admin
- Full access to everything for that domain
- Can create/edit/delete content and settings
- Cannot manage other users' domain permissions from admin panel (superuser-only)

## Usage Patterns

### For Multi-Tenant Hosting

If you're hosting multiple clients, each client gets their own domain with dedicated content:

```
Domain: client-a.com
  ├── Pages (client A only)
  ├── Templates (client A specific)
  ├── Stylesheets (client A specific)
  └── Media Library (client A only)

Domain: client-b.com
  ├── Pages (client B only)
  ├── Templates (client B specific)
  ├── Stylesheets (client B specific)
  └── Media Library (client B only)
```

### For Multi-Brand Single Organization

If you have multiple brands within one organization:

```
Domain: brand-a.example.com
  └── All Brand A content

Domain: brand-b.example.com
  └── All Brand B content

Domain: corporate.example.com
  └── Corporate site content
```

### For Team Collaboration

Assign different roles to team members:

```
User: alice
  ├── example.com → Admin (full control)
  ├── brand-site.com → Editor (can create/edit)
  └── archive.com → Viewer (read-only)

User: bob
  ├── brand-site.com → Editor (can create/edit)
  └── archive.com → Viewer (read-only)
```

## Admin Interface Behavior

### Automatic Filtering

When you log into the admin panel:
- **Superuser**: Sees all domains and content
- **Regular User**: Only sees domains they have permission for
- **Editor**: Sees only content for their assigned domains
- **Viewer**: Sees read-only content for their assigned domains

### Content Creation

When creating new content (pages, templates, media):
- You must select which domain it belongs to
- You can only see domains you have editor+ permissions for
- Content is automatically isolated from other domains

### Domain Switching

To work on a different domain:
1. Go to the Domain section in admin
2. Select the domain you want to work on
3. All content views will filter automatically

## API & View Integration

### Filtering Querysets

In your views, use the utility functions to filter by domain:

```python
from cmsapp.domains.utils import filter_queryset_by_domain, get_user_domains

# Get all pages for domains the user has access to
pages = filter_queryset_by_domain(Page.objects.all(), request.user)

# Get pages for a specific domain
pages = filter_queryset_by_domain(
    Page.objects.all(), 
    request.user, 
    domain=request.domain  # if you pass domain context
)

# Get all domains a user has access to
user_domains = get_user_domains(request.user)
```

### Checking Permissions

```python
from cmsapp.domains.utils import get_user_permissions_for_domain

perm = get_user_permissions_for_domain(request.user, domain)

if perm.has_edit_permission():
    # Allow editing
    
if perm.has_admin_permission():
    # Allow admin actions
```

### View Decorator

Protect views that require domain permissions:

```python
from cmsapp.domains.utils import require_domain_permission

@require_domain_permission(permission_type='edit')
def edit_page(request, page_id, domain=None, user_permission=None):
    # Only editors and admins can access
    # domain and user_permission are injected
    pass
```

## Security Considerations

1. **Data Isolation**: Each domain's content is completely isolated at the database level
2. **Permission Enforcement**: User permissions are checked before any content access
3. **Superuser Access**: Superusers bypass domain restrictions
4. **Audit Trail**: Created/updated timestamps track all changes
5. **Slug Uniqueness**: Slugs are unique per-domain, allowing the same slug on different domains

## Migration from Single Domain

If you're upgrading from a single-domain installation:

1. Create a default domain (e.g., "default")
2. Run the migration (it will create the domain field)
3. Manually assign a default domain to existing content:
   ```python
   from cmsapp.domains.models import Domain
   from cmsapp.pages.models import Page
   
   default_domain = Domain.objects.create(
       name='default',
       title='Default Domain'
   )
   
   Page.objects.all().update(domain=default_domain)
   ```
4. Grant users permissions to the default domain
5. Test thoroughly before going live

## Troubleshooting

### "Domain not found" errors
- Check that the domain exists in Domain Management
- Verify the domain is marked as active (`is_active=True`)
- Ensure you have permission for that domain

### Can't see content in admin
- Verify you have a DomainPermission for that domain
- Check that your permission role is not "Viewer"
- If superuser, check that the domain exists

### Slugs conflicting across domains
- This is expected! Each domain can have pages with the same slug
- URLs will be routed differently by domain

## Future Enhancements

Potential features for future versions:
- Domain-specific user roles and permissions
- Custom domain branding in the frontend
- Domain migration/duplication
- Per-domain analytics
- Domain-specific search indexing
