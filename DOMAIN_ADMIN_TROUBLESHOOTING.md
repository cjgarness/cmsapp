# Domain Editor Admin Access Troubleshooting

If a domain editor cannot see or edit content in the admin console, follow these troubleshooting steps:

## Diagnosis

### 1. Check User Permissions with Management Command

```bash
python manage.py check_domain_permissions <username>
```

Replace `<username>` with the actual username. This command will show:
- Whether the user is a staff member
- Whether the user is a superuser
- All domain permissions assigned to them
- Available domains

**Example:**
```bash
python manage.py check_domain_permissions john_editor
```

### 2. Common Issues and Fixes

#### Issue 1: User is not a staff member

**Error:** "You don't have permission to view or edit anything."

**Fix:** Make the user a staff member:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
user = User.objects.get(username='john_editor')
user.is_staff = True
user.save()
print(f"User {user.username} is now staff: {user.is_staff}")
```

#### Issue 2: No domain permissions assigned

**Error:** User can log in but sees empty admin interface

**Fix:** Assign a domain to the user:

1. **Via Django Admin:**
   - Go to `/admin/domains/domainpermission/`
   - Click "Add Domain Permission"
   - Select the user
   - Select a domain (e.g., "altuspath.com")
   - Choose role: "Editor" (can create/edit) or "Admin" (full control)
   - Check "is_active" checkbox
   - Click Save

2. **Via Django Shell:**

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from cmsapp.domains.models import Domain, DomainPermission

# Get the user and domain
user = User.objects.get(username='john_editor')
domain = Domain.objects.get(name='altuspath.com')

# Create the permission
perm, created = DomainPermission.objects.get_or_create(
    user=user,
    domain=domain,
    defaults={
        'role': 'editor',  # or 'admin', 'viewer'
        'is_active': True
    }
)

if created:
    print(f"Permission created for {user.username} on {domain.name}")
else:
    print(f"Permission already exists for {user.username} on {domain.name}")
    print(f"Current role: {perm.role}, Active: {perm.is_active}")
```

#### Issue 3: Domain permission is inactive (is_active=False)

**Error:** User has permission but still can't access

**Fix:** Activate the permission:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from cmsapp.domains.models import DomainPermission

user = User.objects.get(username='john_editor')
perms = DomainPermission.objects.filter(user=user)

for perm in perms:
    if not perm.is_active:
        perm.is_active = True
        perm.save()
        print(f"Activated permission for {perm.domain.name}")
```

Or via Django Admin:
- Go to `/admin/domains/domainpermission/`
- Find the permission for the user
- Check the "is_active" checkbox
- Click Save

#### Issue 4: Domain is inactive

**Error:** User has permission but domain is inactive

**Fix:** Activate the domain:

1. **Via Django Admin:**
   - Go to `/admin/domains/domain/`
   - Find the domain
   - Check "is_active" checkbox
   - Click Save

2. **Via Django Shell:**

```bash
python manage.py shell
```

```python
from cmsapp.domains.models import Domain

domain = Domain.objects.get(name='altuspath.com')
domain.is_active = True
domain.save()
print(f"Domain {domain.name} is now active")
```

## Verification Steps

After fixing any of the above issues, verify the fix:

```bash
# Check permissions again
python manage.py check_domain_permissions <username>

# Log out and log back in (clear browser session)
# Navigate to /admin/
# You should now see your domains and content
```

## Expected Behavior After Fix

Once properly configured, a domain editor should see:

1. **Admin Dashboard** showing:
   - Their assigned domains
   - Their role for each domain
   - Quick links to manage content

2. **Available Admin Sections** based on their role:
   - **Pages** (can create/edit pages for their domains)
   - **Templates** (if admin role)
   - **Media** (media library for their domains)
   - **Stylesheets** (if admin role)
   - **Domain Permissions** (if admin role)

3. **Content Filtering:**
   - When viewing/editing pages, only their domain's content appears
   - When creating new pages, they can only assign to their domains
   - Related items (templates, stylesheets) are filtered to their domains

## Permission Level Details

### Viewer Role
- Can only view content
- Cannot edit, create, or delete
- Use case: Stakeholders, approval reviewers

### Editor Role (Recommended for most content authors)
- Can create and edit pages, media
- Can manage media library for their domain
- Cannot modify domain settings or templates
- Cannot manage user permissions
- Perfect for: Content authors, editors

### Admin Role (Full control)
- Can do everything an Editor can do
- Can modify domain settings (SEO, features, custom CSS/JS)
- Can manage templates and stylesheets
- Can manage user permissions for their domain (if extended)
- Perfect for: Domain owners, site administrators

## Support

If you continue to have issues:

1. Run the diagnostic command: `python manage.py check_domain_permissions <username>`
2. Check Django logs for any permission-related errors
3. Verify the database has the correct records:
   ```sql
   SELECT * FROM domains_domainpermission WHERE user_id = <user_id>;
   ```
4. Ensure the user has is_staff=True and is_active=True
