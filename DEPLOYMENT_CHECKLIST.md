# Production Deployment - Modern Templates

## Quick Deployment Checklist

### Pre-Deployment
- [ ] Review PRODUCTION_TEMPLATE_FIX.md for details
- [ ] Backup database: `./backup-db-prod.sh`
- [ ] Review changes in git
- [ ] Test locally if possible

### Deployment

#### 1. Pull Latest Code
```bash
git pull origin main
```

#### 2. Apply Migrations
```bash
python manage.py migrate
```

#### 3. Set Up Modern Templates
```bash
python manage.py setup_modern_templates --domain=altuspath.com
```

Output should show:
```
Setting up modern templates for domain: altuspath.com
⊘ Already exists: Modern Contact
⊘ Already exists: Modern Homepage
⊘ Already exists: Modern Page Detail
⊘ Already exists: Modern Page List

Completed! Created 0 templates for altuspath.com
```

#### 4. Apply Modern Stylesheet
```bash
python manage.py apply_modern_stylesheet --domain=altuspath.com
```

Output should show:
```
Applying modern stylesheet to domain: altuspath.com
✓ Created stylesheet: Modern Theme

Stylesheet record applied to altuspath.com
```

#### 5. Create Homepage (if needed)
```bash
python manage.py setup_homepage --domain=altuspath.com
```

Output should show:
```
Setting up homepage for domain: altuspath.com
✓ Created homepage: Welcome to AltusPath

Homepage is ready! Access it at: http://altuspath.com/
```

Or if homepage already exists:
```
Setting up homepage for domain: altuspath.com
⊘ Homepage already exists: Welcome to AltusPath
```

#### 6. Collect Static Files (if needed)
```bash
python manage.py collectstatic --noinput
```

#### 7. Restart Services
```bash
# Docker
docker-compose restart web

# Or systemd
systemctl restart cms-app
```

### Post-Deployment Verification

#### 1. Check Database
```bash
python manage.py shell << 'EOF'
from cmsapp.pages.models import Page
from cmsapp.templates.models import PageTemplate

# Verify homepage exists
homepage = Page.objects.get(is_homepage=True, status='published')
print(f"✓ Homepage: {homepage.title}")
print(f"✓ Template: {homepage.template.name}")
print(f"✓ Template Path: {homepage.template.template_name}")

# Verify all templates
print(f"\n✓ Templates available: {PageTemplate.objects.count()}")
EOF
```

#### 2. Test Homepage
Visit: `https://altuspath.com/`

Expected result:
- No template errors
- Homepage renders with Modern Homepage template
- Navigation bar loads
- Footer displays correctly

#### 3. Check Logs
```bash
# Docker
docker-compose logs -f web

# Or systemd
journalctl -u cms-app -f
```

Look for any template-related errors.

#### 4. Test Other Pages
- Visit `/pages/` - should show page list
- Create a test page and verify it renders

### Rollback (if issues occur)

If you need to revert:

```bash
# Undo migrations
python manage.py migrate templates 0002_initial

# Or revert entire deployment
git revert HEAD
git push origin main
```

## Key Files Changed

- `cmsapp/templates/models.py` - Added template_name field
- `cmsapp/pages/views.py` - Updated to use template_name
- `cmsapp/templates/management/commands/setup_modern_templates.py` - Populates template_name
- `cmsapp/pages/management/commands/setup_homepage.py` - New command to create homepage
- Database migration: `cmsapp/templates/migrations/0003_pagetemplate_template_name_and_more.py`

## Monitoring After Deployment

### Error to Watch For
If you see this error again:
```
django.template.exceptions.TemplateDoesNotExist: templates/page_detail_*.html
```

It means:
1. A page is using old template without template_name
2. The template files were moved or deleted
3. Settings TEMPLATES not configured correctly

### Troubleshooting

**Issue: Templates not found**
- Solution: Verify templates exist in `templates/modern/`
- Command: `ls -la templates/modern/`

**Issue: Homepage shows 404**
- Solution: Ensure homepage is published and template assigned
- Check: `python manage.py shell` then verify Page record exists

**Issue: Static CSS not loading**
- Solution: Run collectstatic
- Command: `python manage.py collectstatic --noinput`

**Issue: Database migration fails**
- Solution: Check for conflicting migrations
- Command: `python manage.py showmigrations templates`

## Support References

- Template System: [MODERN_TEMPLATES_GUIDE.md](MODERN_TEMPLATES_GUIDE.md)
- Template Setup: [MODERN_TEMPLATES_QUICKSTART.md](MODERN_TEMPLATES_QUICKSTART.md)
- Fix Details: [PRODUCTION_TEMPLATE_FIX.md](PRODUCTION_TEMPLATE_FIX.md)

## Success Criteria

After deployment, verify:
- [ ] No template errors in logs
- [ ] Homepage loads at `/`
- [ ] Page detail pages load at `/page-slug/`
- [ ] Page list loads at `/pages/`
- [ ] Styles and navigation display correctly
- [ ] Admin pages work correctly
- [ ] Database migration completed successfully
