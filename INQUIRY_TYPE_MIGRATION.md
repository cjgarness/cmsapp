# Inquiry Type Model Migration - Summary

## Overview
Moved `INQUIRY_TYPE_CHOICES` from hardcoded values in the `ContactInquiry` model to a database-managed `InquiryType` model that is manageable through the Django admin interface on a per-domain basis.

## Changes Made

### 1. New Model: `InquiryType`
- **File**: `cmsapp/contact/models.py`
- **Fields**:
  - `domain` (ForeignKey): Links inquiry types to specific domains
  - `slug` (SlugField): Internal identifier for the inquiry type
  - `label` (CharField): Display name for the inquiry type
  - `order` (PositiveIntegerField): Display order in dropdowns
  - `is_active` (BooleanField): Enable/disable inquiry types
  - `created_at`, `updated_at` (DateTimeField): Timestamps
- **Constraints**:
  - `unique_together`: domain + slug (one slug per domain)
  - Index on: domain + is_active

### 2. Updated Model: `ContactInquiry`
- **Changes**:
  - Removed hardcoded `INQUIRY_TYPE_CHOICES`
  - Added `domain` field (ForeignKey to Domain)
  - Changed `inquiry_type` from CharField to ForeignKey to `InquiryType`
  - Updated all methods to use `inquiry_type.label` instead of `get_inquiry_type_display()`
  - Added index on: domain + status

### 3. Updated Views
- **File**: `cmsapp/contact/views.py`
- Updated to pass `domain` to the form
- Set domain on inquiry before saving

### 4. Updated Forms
- **File**: `cmsapp/contact/forms.py`
- Updated `ContactForm.__init__()` to accept `domain` parameter
- Filters `inquiry_type` queryset by domain and active status
- Falls back to all active inquiry types if no domain provided

### 5. Updated Admin Interface
- **File**: `cmsapp/contact/admin.py`
- Added `InquiryTypeAdmin` to manage inquiry types per domain
- Updated `ContactInquiryAdmin`:
  - Added 'domain' to list_display and fieldsets
  - Updated `inquiry_type_badge()` to work with ForeignKey
  - Updated list_filter to include domain
- `InquiryTypeAdmin` features:
  - Filter by domain and active status
  - Search by label, slug, or domain name
  - Display order and active status

### 6. Database Migrations
- **Migration 0005**: Creates `InquiryType` model and updates `ContactInquiry` structure
- **Migration 0006**: Data migration that:
  - Creates default domain if needed
  - Creates `InquiryType` objects for existing inquiry types
  - Migrates existing contact inquiries to link to new `InquiryType` objects
  - Removes old CharField field

## Migration Instructions

1. **Backup your database** before running migrations:
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate contact
   ```

3. **Verify migration** by checking the admin interface:
   - Go to Django admin
   - Check "Inquiry Types" section to see migrated inquiry types
   - Verify existing contact inquiries still display correctly

## Admin Interface Usage

### Managing Inquiry Types
1. Navigate to Django Admin > Contact > Inquiry Types
2. Create new inquiry types per domain:
   - Select the domain
   - Enter label (display name)
   - Enter slug (internal identifier, must be unique per domain)
   - Set display order
   - Toggle active status
3. Only active inquiry types appear in contact forms

### Viewing Contact Inquiries
1. Navigate to Django Admin > Contact > Contact Inquiries
2. Filter by domain to see inquiries for specific domains
3. Each inquiry shows which domain it came from
4. Inquiry types are now managed centrally in the Inquiry Types section

## Benefits

✅ Inquiry types are now customizable per domain
✅ Managed through Django admin interface
✅ Can enable/disable inquiry types without code changes
✅ Better scalability for multi-domain setups
✅ Easier to add new inquiry types dynamically
✅ Maintains historical data through soft delete (is_active flag)

## Backwards Compatibility Notes

- Old hardcoded inquiry types are automatically migrated to the new system
- Existing contact inquiries are preserved and linked to the new `InquiryType` objects
- Contact form automatically filters inquiry types by the current domain

## Technical Details

### URL Routes
No changes needed - existing routes continue to work

### API/Views
- Contact form automatically filters inquiry types by domain
- No code changes needed in views if domain is properly set in request

### Email Notifications
- Updated to use `inquiry_type.label` instead of `get_inquiry_type_display()`
- SMS notifications also updated to use the new field

## Rollback (if needed)

If you need to rollback these changes:
```bash
python manage.py migrate contact 0004_alter_contactinquiry_inquiry_type
```

This will remove the new `InquiryType` model and revert `ContactInquiry` to use CharField.
