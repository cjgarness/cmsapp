# Modern Templates Setup - Quick Reference

## Management Commands

The modern template system includes two management commands that can now be found and executed by `manage.py`:

### 1. Setup Modern Templates

Creates PageTemplate records for the modern template set in the database.

```bash
python manage.py setup_modern_templates --domain=altuspath.com
```

**What it does:**
- Creates 4 template records in the database:
  - Modern Page Detail (hero layout)
  - Modern Page List (masonry layout)
  - Modern Homepage (hero layout)
  - Modern Contact (single-column layout)
- References the actual template files in `templates/modern/`

**Output:**
```
Setting up modern templates for domain: altuspath.com
✓ Created: Modern Page Detail (file: modern/page_detail.html)
✓ Created: Modern Page List (file: modern/page_list.html)
✓ Created: Modern Homepage (file: modern/homepage.html)
✓ Created: Modern Contact (file: modern/contact.html)

Completed! Created 4 templates for altuspath.com
```

### 2. Apply Modern Stylesheet

Creates a Stylesheet record for the domain.

```bash
python manage.py apply_modern_stylesheet --domain=altuspath.com
```

**What it does:**
- Creates a "Modern Theme" stylesheet record in the database
- Stylesheet is marked as active
- Can be used for domain-specific CSS overrides

**Output:**
```
Applying modern stylesheet to domain: altuspath.com
✓ Created stylesheet: Modern Theme

Stylesheet record applied to altuspath.com

Note: The main CSS is in static/css/modern-base.css
This stylesheet record can contain domain-specific overrides and customizations.
```

## Verification

Check that everything is set up:

```bash
python manage.py shell
```

```python
from cmsapp.domains.models import Domain
from cmsapp.templates.models import PageTemplate, Stylesheet

domain = Domain.objects.get(name='altuspath.com')

# View all templates
for template in domain.page_templates.all():
    print(f"{template.name} - {template.layout_type}")

# View all stylesheets
for stylesheet in domain.stylesheets.all():
    print(f"{stylesheet.name} - Active: {stylesheet.is_active}")
```

## Expected Structure

After running both commands, you should have:

```
Domain: altuspath.com
├── PageTemplates (4)
│   ├── Modern Page Detail
│   ├── Modern Page List
│   ├── Modern Homepage
│   └── Modern Contact
└── Stylesheets (1)
    └── Modern Theme
```

## Template Files

The actual template files are located in:

```
templates/
├── modern/
│   ├── base.html           (Master template - inherited by others)
│   ├── page_detail.html    (Individual page display)
│   ├── page_list.html      (Page grid listing)
│   ├── homepage.html       (Landing page)
│   └── contact.html        (Contact form)
```

## CSS Files

The main styling is in:

```
static/
├── css/
│   └── modern-base.css     (600+ lines of responsive CSS)
└── js/
    └── modern-nav.js       (Mobile menu and animations)
```

## Color Scheme

Nature-inspired bold colors:

| Color | Hex Value | Usage |
|-------|-----------|-------|
| Forest Green | #1b4d3e | Headings, borders |
| Ocean Blue | #0066cc | Links, CTAs, buttons |
| Earth Brown | #8b6f47 | Secondary accents |
| Terracotta | #d97e6e | Alerts, warnings |
| Sky Blue | #87ceeb | Subtle backgrounds |

## Next Steps

1. **Create sample pages** in Django admin:
   - Go to `/admin/pages/page/`
   - Assign pages to "Modern Page Detail" template
   - Publish and view on the site

2. **Customize contact form**:
   - Edit `templates/modern/contact.html` to update contact info
   - Or use Django admin to configure contact settings

3. **Add navigation pages**:
   - Create pages with `show_in_navbar = True`
   - They'll automatically appear in the navigation menu

4. **Customize colors**:
   - Edit CSS variables in `static/css/modern-base.css`
   - Or create domain-specific stylesheet overrides

## Troubleshooting

### Commands not found

Make sure:
1. `cmsapp/templates/management/__init__.py` exists ✓
2. `cmsapp/templates/management/commands/__init__.py` exists ✓
3. Management command files are in proper location ✓

### Domain doesn't exist

Create the domain first:

```bash
python manage.py shell
```

```python
from cmsapp.domains.models import Domain
Domain.objects.create(
    name='altuspath.com',
    title='AltusPath',
    is_active=True
)
```

### File permission errors

The templates don't need to be copied to media folder since they're referenced from the templates directory. The database records store the reference to the template file path.

## File Structure

```
cmsapp/
├── templates/
│   ├── __init__.py
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       ├── setup_modern_templates.py      ← You are here
│   │       └── apply_modern_stylesheet.py     ← And here
│   ├── models.py
│   ├── admin.py
│   └── ...
```

## More Information

See [MODERN_TEMPLATES_GUIDE.md](MODERN_TEMPLATES_GUIDE.md) for comprehensive setup and customization instructions.
