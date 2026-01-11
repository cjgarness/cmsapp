# Command Line Reference

## Deployment Commands

### Pre-Deployment
```bash
# Backup database
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# Check for any issues
python manage.py check
python manage.py migrate --plan contact
```

### Run Migrations
```bash
# Run all pending migrations
python manage.py migrate contact

# Or run specific migration
python manage.py migrate contact 0005
python manage.py migrate contact 0006

# View migration status
python manage.py showmigrations contact
```

### Verification
```bash
# Enter Django shell
python manage.py shell

# Check if data was migrated
from contact.models import InquiryType, ContactInquiry
print(f"Inquiry Types: {InquiryType.objects.count()}")
print(f"Inquiries with domain: {ContactInquiry.objects.exclude(domain__isnull=True).count()}")
print(f"Inquiries with inquiry_type: {ContactInquiry.objects.exclude(inquiry_type__isnull=True).count()}")

# Exit shell
exit()
```

---

## Admin Management Commands

### Create Initial Inquiry Types
```bash
python manage.py shell

from domains.models import Domain
from contact.models import InquiryType

domain = Domain.objects.first()  # or specify: Domain.objects.get(name='example.com')

# Create inquiry types
types = [
    ('question', 'General Question', 0),
    ('service', 'Schedule Service', 1),
    ('feedback', 'Feedback', 2),
    ('other', 'Other', 3),
]

for slug, label, order in types:
    InquiryType.objects.get_or_create(
        domain=domain,
        slug=slug,
        defaults={'label': label, 'order': order, 'is_active': True}
    )

print("✅ Inquiry types created!")
exit()
```

### List All Inquiry Types
```bash
python manage.py shell

from contact.models import InquiryType

for it in InquiryType.objects.all():
    status = "✅" if it.is_active else "⚠️"
    print(f"{status} {it.domain.name} | {it.label} ({it.slug}) | Order: {it.order}")

exit()
```

### List Inquiry Types for Specific Domain
```bash
python manage.py shell

from domains.models import Domain
from contact.models import InquiryType

domain = Domain.objects.get(name='example.com')

for it in domain.inquiry_types.all():
    status = "✅" if it.is_active else "⚠️"
    print(f"{status} {it.label} ({it.slug})")

exit()
```

### Disable an Inquiry Type
```bash
python manage.py shell

from contact.models import InquiryType

# Option 1: By domain and slug
it = InquiryType.objects.get(domain__name='example.com', slug='question')
it.is_active = False
it.save()

# Option 2: By ID
it = InquiryType.objects.get(id=5)
it.is_active = False
it.save()

print("✅ Inquiry type disabled!")
exit()
```

### Enable an Inquiry Type
```bash
python manage.py shell

from contact.models import InquiryType

it = InquiryType.objects.get(domain__name='example.com', slug='service')
it.is_active = True
it.save()

print("✅ Inquiry type enabled!")
exit()
```

### Delete an Inquiry Type (if possible)
```bash
python manage.py shell

from contact.models import InquiryType

try:
    it = InquiryType.objects.get(id=5)
    it.delete()
    print("✅ Inquiry type deleted!")
except Exception as e:
    print(f"❌ Cannot delete: {e}")
    print("Use is_active=False to disable instead")

exit()
```

### Update Inquiry Type Order
```bash
python manage.py shell

from contact.models import InquiryType

# Update specific inquiry type order
it = InquiryType.objects.get(domain__name='example.com', slug='question')
it.order = 1
it.save()

# Or bulk update
InquiryType.objects.filter(domain__name='example.com').update(order=0)

print("✅ Order updated!")
exit()
```

---

## Data Analysis Commands

### Count Inquiries by Type
```bash
python manage.py shell

from contact.models import ContactInquiry
from django.db.models import Count

results = ContactInquiry.objects.values(
    'inquiry_type__label'
).annotate(
    count=Count('id')
).order_by('-count')

for result in results:
    print(f"{result['inquiry_type__label']}: {result['count']}")

exit()
```

### Count Inquiries by Domain
```bash
python manage.py shell

from contact.models import ContactInquiry
from django.db.models import Count

results = ContactInquiry.objects.values(
    'domain__name'
).annotate(
    count=Count('id')
).order_by('-count')

for result in results:
    print(f"{result['domain__name']}: {result['count']}")

exit()
```

### Count Inquiries by Domain AND Type
```bash
python manage.py shell

from contact.models import ContactInquiry
from django.db.models import Count

results = ContactInquiry.objects.values(
    'domain__name',
    'inquiry_type__label'
).annotate(
    count=Count('id')
).order_by('domain__name', '-count')

for result in results:
    print(f"{result['domain__name']} - {result['inquiry_type__label']}: {result['count']}")

exit()
```

### Find Inquiries without Domain (anomaly check)
```bash
python manage.py shell

from contact.models import ContactInquiry

bad_inquiries = ContactInquiry.objects.filter(domain__isnull=True)
print(f"Inquiries without domain: {bad_inquiries.count()}")

for inquiry in bad_inquiries[:5]:  # Show first 5
    print(f"- ID {inquiry.id}: {inquiry.name} ({inquiry.created_at})")

exit()
```

### Find Inquiries without Inquiry Type (anomaly check)
```bash
python manage.py shell

from contact.models import ContactInquiry

bad_inquiries = ContactInquiry.objects.filter(inquiry_type__isnull=True)
print(f"Inquiries without inquiry_type: {bad_inquiries.count()}")

for inquiry in bad_inquiries[:5]:  # Show first 5
    print(f"- ID {inquiry.id}: {inquiry.name} ({inquiry.created_at})")

exit()
```

---

## Export/Backup Commands

### Export Inquiry Types as JSON
```bash
python manage.py dumpdata contact.InquiryType --indent 2 > inquiry_types_backup.json
```

### Export Contact Inquiries as JSON
```bash
python manage.py dumpdata contact.ContactInquiry --indent 2 > contact_inquiries_backup.json
```

### Export Both
```bash
python manage.py dumpdata contact --indent 2 > contact_full_backup.json
```

### Load from JSON (restore)
```bash
python manage.py loaddata contact_full_backup.json
```

---

## Testing Commands

### Run Contact App Tests
```bash
python manage.py test contact
python manage.py test contact.tests.ContactInquiryTestCase -v 2
```

### Test Contact Form with Domain
```bash
python manage.py shell

from contact.forms import ContactForm
from domains.models import Domain

domain = Domain.objects.first()
form = ContactForm(domain=domain)

# Check if inquiry types are filtered
print(f"Available inquiry types: {list(form.fields['inquiry_type'].queryset)}")

exit()
```

### Test Inquiry Type Query
```bash
python manage.py shell

from contact.models import InquiryType
from domains.models import Domain

domain = Domain.objects.first()

# Get active inquiry types for domain
active_types = InquiryType.objects.filter(domain=domain, is_active=True)
print(f"Active types for {domain.name}: {list(active_types)}")

exit()
```

---

## Troubleshooting Commands

### Check Migration Dependencies
```bash
python manage.py migrate --plan contact 0006
```

### Show All Migrations
```bash
python manage.py showmigrations contact
```

### Rollback Migrations (if needed)
```bash
# Rollback to specific migration
python manage.py migrate contact 0004

# Rollback one step
python manage.py migrate contact 0005
```

### Check Database Schema
```bash
python manage.py sqlmigrate contact 0005
python manage.py sqlmigrate contact 0006
```

### Validate Database
```bash
python manage.py check
python manage.py migrate --plan  # Shows all pending migrations
```

### Debug Inquiry Type Creation
```bash
python manage.py shell

from contact.models import InquiryType
from domains.models import Domain

domain = Domain.objects.first()

# Create with debugging
try:
    it = InquiryType.objects.create(
        domain=domain,
        slug='test-type',
        label='Test Type',
        order=99,
        is_active=True
    )
    print(f"✅ Created: {it}")
except Exception as e:
    print(f"❌ Error: {e}")

exit()
```

---

## Performance Monitoring

### Show Slow Queries (in DEBUG mode)
```bash
python manage.py shell

from django.db import connection
from django.test.utils import override_settings

# Enable query logging
from django.db import connection
print(f"Database: {connection.settings_dict['ENGINE']}")
print(f"Queries executed: {len(connection.queries)}")

for query in connection.queries:
    print(f"\nTime: {query['time']}s")
    print(f"SQL: {query['sql']}")

exit()
```

### Count Database Queries
```bash
python manage.py shell

from contact.models import ContactInquiry
from django.db import connection

# Execute query
inquiries = list(ContactInquiry.objects.all())

print(f"Database queries: {len(connection.queries)}")
for i, query in enumerate(connection.queries, 1):
    print(f"{i}. {query['sql'][:100]}...")

exit()
```

---

## Quick Health Check Script

```bash
python manage.py shell << 'EOF'
from contact.models import InquiryType, ContactInquiry
from domains.models import Domain

print("📊 Health Check Report")
print("=" * 50)

domains = Domain.objects.count()
print(f"✅ Domains: {domains}")

inquiry_types = InquiryType.objects.count()
print(f"✅ Inquiry Types: {inquiry_types}")

inquiries = ContactInquiry.objects.count()
print(f"✅ Contact Inquiries: {inquiries}")

inquiries_with_domain = ContactInquiry.objects.exclude(domain__isnull=True).count()
print(f"✅ Inquiries with domain: {inquiries_with_domain}")

inquiries_with_type = ContactInquiry.objects.exclude(inquiry_type__isnull=True).count()
print(f"✅ Inquiries with inquiry_type: {inquiries_with_type}")

if inquiries_with_domain == inquiries and inquiries_with_type == inquiries:
    print("\n✅ All data migrated successfully!")
else:
    print("\n⚠️  Some inquiries may be missing domain or inquiry_type")

print("=" * 50)
EOF
```

---

**All commands are ready to use in production!**
