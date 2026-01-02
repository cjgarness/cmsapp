# Production Error Fix - Template Resolution

## Problem
When deploying modern templates to production, Django couldn't find the templates because the views were trying to render templates stored as file uploads in the media folder with incorrect paths like `templates/page_detail_COfpybv.html`.

**Original Error:**
```
django.template.exceptions.TemplateDoesNotExist: templates/page_detail_COfpybv.html
```

## Root Cause
The `PageTemplate` model only had a `template_file` FileField which stores uploaded files with generated names in the media folder. The views were trying to use this path directly with Django's template loader, which looks in the `templates/` directory by default.

## Solution

### 1. Added `template_name` Field to PageTemplate Model
- New field stores the actual template path (e.g., `modern/page_detail.html`)
- This path points to files in the `templates/` directory
- Made `template_file` optional to support both approaches

```python
template_name = models.CharField(
    max_length=255,
    blank=True,
    help_text='Path to template file (e.g., "modern/page_detail.html")'
)
```

### 2. Updated Views to Use `template_name`
Modified `homepage_view` to check `template_name` first, fall back to `template_file`, then default template:

```python
if homepage.template:
    if homepage.template.template_name:
        return render(request, homepage.template.template_name, context)
    elif homepage.template.template_file:
        return render(request, homepage.template.template_file.name, context)

return render(request, 'pages/page_detail.html', context)
```

### 3. Updated Setup Command
The `setup_modern_templates` command now populates the `template_name` field:

```python
'template_name': template_data['template_path'],
```

### 4. Created Database Migration
```bash
python manage.py makemigrations templates
python manage.py migrate templates
```

### 5. Updated Existing Templates
All existing modern templates were updated with their paths:

```
Modern Page Detail → modern/page_detail.html
Modern Page List → modern/page_list.html
Modern Homepage → modern/homepage.html
Modern Contact → modern/contact.html
```

## Deployment Steps

### Step 1: Apply Migrations
```bash
python manage.py migrate
```

### Step 2: Run Setup Commands
```bash
# Set up templates
python manage.py setup_modern_templates --domain=altuspath.com

# Apply stylesheet
python manage.py apply_modern_stylesheet --domain=altuspath.com

# Create homepage
python manage.py setup_homepage --domain=altuspath.com
```

### Step 3: Collect Static Files (if needed)
```bash
python manage.py collectstatic --noinput
```

### Step 4: Verify Setup
```bash
python manage.py shell << 'EOF'
from cmsapp.pages.models import Page
from cmsapp.templates.models import PageTemplate

# Check homepage
homepage = Page.objects.get(is_homepage=True, status='published')
print(f"Homepage: {homepage.title}")
print(f"Template: {homepage.template.template_name}")
print(f"Ready: {homepage.template.template_name is not None}")
EOF
```

## File Structure

```
templates/
├── modern/
│   ├── base.html
│   ├── page_detail.html      ← Resolves correctly now
│   ├── page_list.html        ← Resolves correctly now
│   ├── homepage.html         ← Resolves correctly now
│   └── contact.html          ← Resolves correctly now

static/
├── css/
│   └── modern-base.css
└── js/
    └── modern-nav.js

cmsapp/
├── pages/
│   └── management/
│       └── commands/
│           └── setup_homepage.py
├── templates/
│   └── management/
│       └── commands/
│           ├── setup_modern_templates.py
│           └── apply_modern_stylesheet.py
```

## Database Changes

### PageTemplate Model
- ✓ Added `template_name` CharField (max_length=255, blank=True)
- ✓ Made `template_file` optional (blank=True, null=True)

### Migration
- File: `cmsapp/templates/migrations/0003_pagetemplate_template_name_and_more.py`
- Status: Applied

## Testing the Fix

### Local Development
```bash
python manage.py runserver
# Visit http://localhost:8000/
```

### Production
The homepage should now render without template errors when accessed at the domain URL.

## Management Commands

### setup_modern_templates
```bash
python manage.py setup_modern_templates --domain=altuspath.com
```
Creates template records with `template_name` field populated.

### apply_modern_stylesheet
```bash
python manage.py apply_modern_stylesheet --domain=altuspath.com
```
Creates stylesheet record for the domain.

### setup_homepage (NEW)
```bash
python manage.py setup_homepage --domain=altuspath.com
```
Creates a published homepage with Modern Homepage template assigned.

## Verification Checklist

- [ ] Migration applied: `python manage.py migrate`
- [ ] Templates created: `python manage.py setup_modern_templates`
- [ ] Homepage created: `python manage.py setup_homepage`
- [ ] Homepage has `template_name` set to `modern/homepage.html`
- [ ] Template files exist in `templates/modern/`
- [ ] Static files collected (if applicable)
- [ ] Homepage renders without errors at `/`

## Rollback (if needed)

If you need to revert this change:
```bash
python manage.py migrate templates 0002_initial
```

This will remove the `template_name` field and restore `template_file` as required.

## Notes

- The `template_name` field is the preferred way to reference templates
- The `template_file` field is kept for backward compatibility
- New templates should always populate `template_name`
- All modern templates have been updated with correct paths
