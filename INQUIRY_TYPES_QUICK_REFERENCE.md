# Quick Reference: Managing Inquiry Types

## For Administrators

### Add a New Inquiry Type for a Domain

1. Go to **Django Admin** → **Contact** → **Inquiry Types**
2. Click **Add Inquiry Type**
3. Fill in the form:
   - **Domain**: Select the domain this inquiry type belongs to
   - **Label**: The name users will see (e.g., "General Question", "Technical Support")
   - **Slug**: Internal identifier, lowercase with hyphens (e.g., "general-question", "tech-support")
   - **Order**: Display position (lower numbers appear first)
   - **Is Active**: Check to make this option available in contact forms
4. Click **Save**

### Edit or Disable an Inquiry Type

1. Go to **Django Admin** → **Contact** → **Inquiry Types**
2. Click on the inquiry type to edit
3. Make changes and click **Save**
4. To hide it from forms without deleting: uncheck **Is Active** and save

### Delete an Inquiry Type

1. Go to **Django Admin** → **Contact** → **Inquiry Types**
2. Click on the inquiry type
3. Click **Delete** at the bottom
   - ⚠️ Note: You can only delete if no inquiries are using it (on_delete=PROTECT)
   - Alternative: Use "Is Active" checkbox to hide it instead

## For Developers

### Default Inquiry Types (Auto-Created on Migration)

When you run the migration, these inquiry types are automatically created:

| Slug | Label | Order |
|------|-------|-------|
| `question` | General Question | 0 |
| `service` | Schedule An Inspection or Service | 1 |
| `feedback` | Feedback | 2 |
| `other` | Other | 3 |

### Accessing Inquiry Types in Code

```python
# Get inquiry types for a specific domain
from contact.models import InquiryType
types = InquiryType.objects.filter(domain=domain, is_active=True)

# Get a specific inquiry type
inquiry_type = InquiryType.objects.get(domain=domain, slug='question')

# Create a new one programmatically
InquiryType.objects.create(
    domain=domain,
    slug='partnership',
    label='Partnership Opportunity',
    order=4,
    is_active=True
)
```

### Using in Contact Form View

```python
# The form automatically filters by domain
from contact.forms import ContactForm

# Pass domain to form
form = ContactForm(domain=request.domain)

# In template, the select will only show active types for that domain
```

### Accessing Inquiry Type in Templates

```django
{# In contact inquiry detail or list #}
{{ inquiry.inquiry_type.label }}
{{ inquiry.inquiry_type.slug }}
{{ inquiry.domain.name }}
```

## Data Model Relationships

```
Domain (1) ─── (Many) InquiryType
                           │
                           └─── (Many) ContactInquiry
```

- Each **Domain** can have multiple **InquiryType** options
- Each **ContactInquiry** belongs to exactly one **Domain** and one **InquiryType**
- Deleting a domain cascades to delete its inquiry types
- Deleting an inquiry type is protected (won't delete if inquiries reference it)

## Common Tasks

### Set Up Inquiry Types for a New Domain

1. Create the domain in **Django Admin** → **Domains**
2. Go to **Inquiry Types** → **Add Inquiry Type**
3. For each inquiry type you want:
   - Select your new domain
   - Fill in label and slug
   - Click Save
4. Users can now select from these types in the contact form

### Clone Inquiry Types from One Domain to Another

```python
from contact.models import InquiryType

source_domain = Domain.objects.get(name='source.com')
target_domain = Domain.objects.get(name='target.com')

# Copy active inquiry types
for inquiry_type in source_domain.inquiry_types.filter(is_active=True):
    InquiryType.objects.create(
        domain=target_domain,
        slug=inquiry_type.slug,
        label=inquiry_type.label,
        order=inquiry_type.order,
        is_active=inquiry_type.is_active
    )
```

### Export/Backup Inquiry Types

```python
import json
from django.core import serializers

# Serialize all inquiry types as JSON
data = serializers.serialize('json', InquiryType.objects.all())
with open('inquiry_types_backup.json', 'w') as f:
    f.write(data)
```

### View All Inquiry Types with Their Domain

In Django Admin, the list view shows:
- **Label**: The display name
- **Domain**: Which domain it belongs to
- **Slug**: Internal identifier
- **Order**: Display position
- **Is Active**: Whether it's available
- **Created at**: When it was created

Filter and search options are available in the admin interface.
