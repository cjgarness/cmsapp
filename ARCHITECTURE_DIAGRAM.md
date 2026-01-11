# Architecture & Data Flow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Django Admin Interface                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────┐  ┌────────────────────────────────┐   │
│  │  Inquiry Types      │  │  Contact Inquiries             │   │
│  │  Management         │  │  View & Edit                   │   │
│  │                     │  │                                │   │
│  │ • Add new types    │  │ • Filter by domain             │   │
│  │ • Edit label       │  │ • Filter by inquiry type       │   │
│  │ • Set order        │  │ • Mark as read/responded       │   │
│  │ • Enable/disable   │  │ • Manage statuses              │   │
│  │ • View history     │  │ • View email notifications     │   │
│  └─────────────────────┘  └────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
         ↓                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Database Layer                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────┐  ┌─────────────────────────┐  │
│  │      domains_domain          │  │  contact_inquirytype   │  │
│  ├──────────────────────────────┤  ├─────────────────────────┤  │
│  │ • id (PK)                   │  │ • id (PK)              │  │
│  │ • name                      │  │ • domain_id (FK)       │  │
│  │ • title                     │  │ • slug (unique)        │  │
│  │ • contact_email             │  │ • label                │  │
│  │ • contact_phone             │  │ • order                │  │
│  │ • is_active                 │  │ • is_active            │  │
│  │ • created_at                │  │ • created_at           │  │
│  │ • updated_at                │  │ • updated_at           │  │
│  └──────────────────────────────┘  └─────────────────────────┘  │
│         ▲                                      ▲                 │
│         │ 1                                    │ N              │
│         │───────────────────────────────────────│                │
│         └─ Has many                                              │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │         contact_contactinquiry                             │  │
│  ├────────────────────────────────────────────────────────────┤  │
│  │ • id (PK)                                                  │  │
│  │ • domain_id (FK)          ─────→ domains_domain.id         │  │
│  │ • inquiry_type_id (FK)    ─────→ contact_inquirytype.id   │  │
│  │ • name                                                     │  │
│  │ • email                                                    │  │
│  │ • phone                                                    │  │
│  │ • message                                                  │  │
│  │ • status                                                   │  │
│  │ • admin_notes                                              │  │
│  │ • created_at                                               │  │
│  │ • updated_at                                               │  │
│  │ • read_at                                                  │  │
│  │ • responded_at                                             │  │
│  │                                                             │  │
│  │ Indexes:                                                    │  │
│  │ • (domain_id, status)                                      │  │
│  │ • (domain_id, inquiry_type_id)                             │  │
│  │ • (-created_at)                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
         ▲
         │
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌────────────────────┐  ┌─────────────┐ │
│  │  views.py        │  │  forms.py          │  │ models.py   │ │
│  ├──────────────────┤  ├────────────────────┤  ├─────────────┤ │
│  │ contact()        │  │ ContactForm()      │  │ InquiryType │ │
│  │                  │  │                    │  │ (new)       │ │
│  │ • Get domain     │  │ • Accept domain    │  │             │ │
│  │ • Create form    │  │ • Filter inquiry   │  │ ContactInq  │ │
│  │ • Handle POST    │  │   types by domain  │  │ (updated)   │ │
│  │ • Save inquiry   │  │ • Validate form    │  │             │ │
│  │ • Send emails    │  │                    │  │ Contains:   │ │
│  │ • Set domain     │  │ widgets:           │  │ • FK domain │ │
│  │ • Send SMS       │  │ • TextInput        │  │ • FK type   │ │
│  │                  │  │ • EmailInput       │  │ • Status    │ │
│  │                  │  │ • Select (types)   │  │             │ │
│  │                  │  │ • Textarea         │  │ Methods:    │ │
│  │                  │  │                    │  │ • save_conf │ │
│  │                  │  │                    │  │ • send_alert│ │
│  │                  │  │                    │  │ • send_sms  │ │
│  └──────────────────┘  └────────────────────┘  └─────────────┘ │
│         ▲                       ▲                       ▲         │
│         └───────────────────────┴───────────────────────┘        │
│                  All coordinated by Django                       │
└─────────────────────────────────────────────────────────────────┘
         ▲
         │
┌─────────────────────────────────────────────────────────────────┐
│                      User Interface Layer                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Contact Form (User-Facing)                 │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │                                                         │   │
│  │  Name: ___________________________                      │   │
│  │  Email: __________________________                     │   │
│  │  Phone: __________________________                     │   │
│  │  Inquiry Type: ▼ (Domain-Filtered!) ◄─── InquiryType │   │
│  │    - General Question                                 │   │
│  │    - Technical Support                                │   │
│  │    - Schedule Service                                 │   │
│  │    - Feedback                                         │   │
│  │                                                         │   │
│  │  Message: _____________________________                │   │
│  │          _____________________________                │   │
│  │          _____________________________                │   │
│  │                                                         │   │
│  │          [  Submit Inquiry  ]                         │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                         ▼                                        │
│           [Inquiry Stored with Domain & Type]                  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
User Visits Contact Form
         │
         ↓
Request Middleware (sets request.domain)
         │
         ↓
Contact View (views.py)
  ├─ Gets domain from request
  ├─ Gets contact configuration
  └─ Creates ContactForm(domain=domain)
         │
         ↓
ContactForm.__init__(domain=domain)
  ├─ Filters InquiryType objects
  │  └─ filter(domain=domain, is_active=True)
  ├─ Sets queryset for inquiry_type field
  └─ Form is ready for display
         │
         ↓
Template Renders Form
  └─ inquiry_type dropdown shows only
     domain-specific active types
         │
         ↓
User Selects Options & Submits
         │
         ↓
POST Request to Contact View
         │
         ↓
ContactForm Validation
  ├─ Validates all required fields
  ├─ Ensures inquiry_type is in filtered queryset
  └─ form.is_valid() = True
         │
         ↓
Save Inquiry
  ├─ inquiry = form.save(commit=False)
  ├─ inquiry.domain = request.domain [CRITICAL]
  ├─ inquiry.save()
  └─ Inquiry stored with domain & inquiry_type
         │
         ├─────────────────────┬──────────────┬─────────────┐
         ↓                     ↓              ↓             ↓
    Send Confirmation  Send Alert Email  Send SMS     Redirect
    to User Email      to Admin Email    to Admin      to Thank You
         │
         ↓
   Inquiry Visible in Django Admin
   • Filter by domain
   • Filter by inquiry_type
   • View all details
   • Respond and track status
```

---

## Request Processing Flow

```
HTTP Request (GET /contact/)
    │
    ↓
Domain Middleware
    │
    ├─ Detects domain from request
    ├─ Sets request.domain = Domain object
    └─ Request continues
    │
    ↓
contact() View
    │
    ├─ request.method == 'GET'
    │   ├─ domain = getattr(request, 'domain', None)
    │   ├─ form = ContactForm(domain=domain)
    │   └─ render template with form
    │
    └─ request.method == 'POST'
        ├─ domain = getattr(request, 'domain', None)
        ├─ form = ContactForm(request.POST, domain=domain)
        │
        ├─ form.is_valid()
        │   │
        │   ├─ inquiry = form.save(commit=False)
        │   ├─ inquiry.domain = domain
        │   ├─ inquiry.save()
        │   │
        │   ├─ Send confirmation email
        │   ├─ Send admin alert
        │   ├─ Send SMS (if enabled)
        │   │
        │   └─ redirect('thank_you')
        │
        └─ form.is_valid() == False
            ├─ Show form with errors
            └─ re-render template
```

---

## Database Query Flow

```
ContactForm Initialization
    │
    ├─ __init__(domain=request.domain)
    │
    ├─ InquiryType.objects.filter(
    │      domain=domain,
    │      is_active=True
    │   ).order_by('order', 'label')
    │
    └─ Set inquiry_type field queryset
         │
         ↓
    Template Renders Select
         │
         ├─ For each InquiryType in queryset:
         │   <option value="{inquiry_type.id}">
         │     {inquiry_type.label}
         │   </option>
         │
         └─ Only domain-specific types shown!
         
After Submission
    │
    ├─ form.save(commit=False)
    │   └─ Creates ContactInquiry instance (not saved)
    │
    ├─ Set domain and inquiry_type from form
    │   └─ inquiry.domain = domain
    │   └─ inquiry.inquiry_type = selected InquiryType
    │
    ├─ inquiry.save()
    │   └─ INSERT into contact_contactinquiry
    │       (name, email, phone, domain_id, inquiry_type_id, ...)
    │
    └─ Query Database for Emails
        └─ InquiryType.objects.get(id=inquiry_type_id)
           └─ Access inquiry_type.label for email subject
```

---

## Multi-Tenant Support

```
Domain A (example-a.com)
  │
  ├─ InquiryType: "Question" (slug: question)
  ├─ InquiryType: "Support" (slug: support)
  ├─ InquiryType: "Sales" (slug: sales)
  │
  └─ ContactInquiry
      ├─ domain_id = Domain A
      ├─ inquiry_type_id = InquiryType A.question
      └─ ...

Domain B (example-b.com)
  │
  ├─ InquiryType: "General" (slug: general)
  ├─ InquiryType: "Technical" (slug: technical)
  │
  └─ ContactInquiry
      ├─ domain_id = Domain B
      ├─ inquiry_type_id = InquiryType B.general
      └─ ...

Data Isolation:
  • Each domain sees only its inquiry types
  • Forms filter by domain automatically
  • Admin can see all domains
  • Reports can be generated per domain
```

---

## Performance Considerations

```
Database Indexes:
├─ contact_inquirytype
│  └─ (domain_id, is_active)
│     └─ Fast filtering of active types per domain
│
└─ contact_contactinquiry
   ├─ (-created_at)
   │  └─ Fast sorting by newest first
   ├─ (domain_id, status)
   │  └─ Fast filtering by domain & status
   └─ Foreign key indexes
      └─ Fast lookups & joins

Query Optimization:
├─ Form initialization queries once
├─ Template doesn't re-query
├─ Admin uses select_related()
└─ Efficient joins on ForeignKeys
```

---

## Error Handling Flow

```
Form Submission
    │
    ├─ ContactForm validation
    │   │
    │   ├─ Required fields missing?
    │   │   └─ Show form with errors
    │   │
    │   ├─ Invalid email?
    │   │   └─ Show form with errors
    │   │
    │   └─ Invalid inquiry_type selection?
    │       └─ Show form with errors
    │
    ├─ Save to database
    │   │
    │   ├─ Database error?
    │   │   └─ Log error, show generic message
    │   │
    │   └─ Success
    │       └─ Create inquiry
    │
    ├─ Send notifications
    │   │
    │   ├─ Confirmation email error?
    │   │   └─ Log error, continue
    │   │
    │   ├─ Alert email error?
    │   │   └─ Log error, continue
    │   │
    │   ├─ SMS error?
    │   │   └─ Log error, continue
    │   │
    │   └─ All notifications sent/attempted
    │
    └─ Redirect to thank you
        └─ User sees confirmation
```

---

## Migration Architecture

```
Phase 1: Schema Creation (0005)
    │
    ├─ CREATE TABLE contact_inquirytype
    │   ├─ id, domain_id, slug, label, order, is_active
    │   ├─ created_at, updated_at
    │   └─ Unique constraint (domain_id, slug)
    │
    ├─ ALTER TABLE contact_contactinquiry
    │   ├─ ADD domain_id (nullable)
    │   ├─ RENAME inquiry_type → inquiry_type_old
    │   ├─ ADD inquiry_type_id (nullable, FK)
    │   └─ Add index (domain_id, status)
    │
    └─ Tables now prepared for data

Phase 2: Data Migration (0006)
    │
    ├─ Create default domain (if needed)
    │
    ├─ Create InquiryType objects
    │   ├─ For each original type:
    │   │   ├─ ('question', 'General Question')
    │   │   ├─ ('service', 'Schedule Service')
    │   │   ├─ ('feedback', 'Feedback')
    │   │   └─ ('other', 'Other')
    │   │
    │   └─ Link all to default domain
    │
    ├─ Migrate existing ContactInquiry records
    │   ├─ For each inquiry:
    │   │   ├─ Get original inquiry_type_old value
    │   │   ├─ Find matching InquiryType
    │   │   ├─ Set domain = default_domain
    │   │   ├─ Set inquiry_type = matched InquiryType
    │   │   └─ Save updated inquiry
    │   │
    │   └─ All inquiries now linked
    │
    ├─ Remove old field
    │   └─ ALTER TABLE DROP inquiry_type_old
    │
    └─ Make new fields non-nullable
        ├─ ALTER TABLE ALTER domain_id NOT NULL
        └─ ALTER TABLE ALTER inquiry_type_id NOT NULL

Result: Fully migrated data with proper relationships
```

---

This architecture ensures:
✅ Clean separation of concerns
✅ Multi-tenant data isolation
✅ Efficient database queries
✅ Proper foreign key relationships
✅ Scalable design
✅ Easy to maintain and extend
