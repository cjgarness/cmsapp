# Contact Form IntegrityError Fix

## Problem
The contact form was throwing an `IntegrityError` when submitting inquiries:
```
IntegrityError at /contact/
null value in column "inquiry_type_old" of relation "contact_contactinquiry" violates not-null constraint
```

## Root Cause
The database table `contact_contactinquiry` had a field `inquiry_type_old` with a NOT NULL constraint, but:
1. This field was not defined in the Django model (`ContactInquiry`)
2. The form did not populate this field when saving records
3. Django's migration state was out of sync with the actual database schema

## Solution
Implemented a 3-part fix:

### 1. Updated Django Model ([cmsapp/contact/models.py](cmsapp/contact/models.py))
Added the `inquiry_type_old` field to the `ContactInquiry` model:
```python
inquiry_type_old = models.CharField(
    max_length=50,
    default='general',
    help_text="Deprecated: Use inquiry_type ForeignKey instead"
)
```

This field stores the original string-based inquiry type for backwards compatibility while the new code uses the `inquiry_type` ForeignKey.

### 2. Synced Django Migrations
Created migration `0007_sync_inquiry_type_old_field.py` to register the existing database field with Django's migration state (faked since the field already existed).

### 3. Updated Contact Form ([cmsapp/contact/forms.py](cmsapp/contact/forms.py))
Modified the `ContactForm.save()` method to automatically populate `inquiry_type_old` from the selected `inquiry_type`:
```python
def save(self, commit=True):
    instance = super().save(commit=False)
    
    # Populate inquiry_type_old with the slug of the selected inquiry_type
    if instance.inquiry_type:
        instance.inquiry_type_old = instance.inquiry_type.slug
    else:
        instance.inquiry_type_old = 'general'
    
    if commit:
        instance.save()
    
    return instance
```

## Files Changed
- [cmsapp/contact/models.py](cmsapp/contact/models.py) - Added `inquiry_type_old` field
- [cmsapp/contact/forms.py](cmsapp/contact/forms.py) - Added automatic population of `inquiry_type_old`
- [cmsapp/contact/migrations/0007_sync_inquiry_type_old_field.py](cmsapp/contact/migrations/0007_sync_inquiry_type_old_field.py) - Synced migration state

## Verification
✅ Database field exists with NOT NULL constraint
✅ Django model includes the field definition
✅ Form validation passes
✅ Records save successfully without IntegrityError
✅ Test submission with form data works correctly

## Migration Instructions
1. Apply the migration: `python manage.py migrate contact`
2. The form will now automatically populate `inquiry_type_old` when saving submissions
3. No data loss - existing records remain intact
