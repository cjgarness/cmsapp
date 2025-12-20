# 🚀 QUICK REFERENCE GUIDE

## ⚡ 30-Second Start (Windows)

```cmd
cd c:\dev\vscode\cmsapp
build-dev.bat
```

Then open: **http://localhost:8000**

## ⚡ 30-Second Start (Linux/Mac)

```bash
cd /path/to/cmsapp
chmod +x build-dev.sh
./build-dev.sh
```

Then open: **http://localhost:8000**

---

## 📋 First Things First

| What | Action |
|------|--------|
| **See project overview** | Read [SUMMARY.md](SUMMARY.md) |
| **Get running quickly** | Follow [QUICKSTART.md](QUICKSTART.md) |
| **Full documentation** | Read [README.md](README.md) |
| **Production setup** | Read [DEPLOYMENT.md](DEPLOYMENT.md) |
| **File listing** | Check [INDEX.md](INDEX.md) |

---

## 🔑 Key URLs

| URL | Purpose | When |
|-----|---------|------|
| http://localhost:8000 | Website | Dev |
| http://localhost:8000/admin | Admin Panel | Dev |
| http://localhost:8000/api/health | API Health | Dev |
| http://localhost | Website | Prod |
| http://localhost/admin | Admin Panel | Prod |
| http://localhost/api/health | API Health | Prod |

---

## 🐳 Essential Docker Commands

### View Running Containers
```bash
docker-compose -f docker-compose.dev.yml ps
```

### View Application Logs
```bash
docker-compose -f docker-compose.dev.yml logs -f web
```

### Access Database
```bash
docker-compose -f docker-compose.dev.yml exec db psql -U cmsuser -d cmsdb
```

### Access Django Shell
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py shell
```

### Create Superuser
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

### Stop Services
```bash
docker-compose -f docker-compose.dev.yml down
```

---

## 🛠️ Common Management Tasks

### Create Admin User
```bash
./manage-cms.sh dev createsuperuser  # Linux/Mac
manage-cms.bat dev createsuperuser   # Windows
```

### Database Migrations
```bash
./migrate.sh dev make      # Create
./migrate.sh dev migrate   # Apply
./migrate.sh dev show      # Status
```

### Collect Static Files
```bash
./manage-cms.sh dev staticfiles
```

### Access Django Shell
```bash
./manage-cms.sh dev shell
```

### Clear Cache
```bash
./manage-cms.sh dev clearcache
```

---

## 📁 File Locations

| Purpose | Path |
|---------|------|
| **Django Settings** | cmsapp/settings.py |
| **URLs** | cmsapp/urls.py, cmsapp/pages/urls.py |
| **Models** | cmsapp/pages/models.py, cmsapp/templates/models.py |
| **Views** | cmsapp/pages/views.py |
| **Admin** | cmsapp/pages/admin.py |
| **Templates** | templates/ |
| **Styles** | static/css/style.css |
| **JavaScript** | static/js/main.js |
| **Environment** | .env |
| **Database Config** | docker-compose.dev.yml |

---

## 🎯 First Task: Create a Page

1. Go to **http://localhost:8000/admin**
2. Login with your superuser credentials
3. Click **Pages** → **Add Page**
4. Fill in:
   - **Title**: My First Page
   - **Content**: Welcome to my CMS!
   - **Status**: Published
5. Click **Save**
6. Visit **http://localhost:8000/my-first-page**

---

## 🎨 Second Task: Upload a Stylesheet

1. Go to **Admin** → **Templates** → **Stylesheets**
2. Click **Add Stylesheet**
3. Upload a CSS file
4. Fill in **name** and **description**
5. Check **is active**
6. Click **Save**

---

## 📸 Third Task: Add Media

1. Go to **Admin** → **Media** → **Media Files**
2. Click **Add Media File**
3. Upload an image
4. Fill in **title** and **description**
5. Click **Save**

---

## 🚀 Deploy to Production

```bash
./build-prod.sh        # Linux/Mac
build-prod.bat        # Windows
```

Then follow [DEPLOYMENT.md](DEPLOYMENT.md) for SSL setup.

---

## 🔒 Security Checklist Before Production

- [ ] Change `SECRET_KEY` in .env
- [ ] Set `DEBUG=False` in .env
- [ ] Use strong database password
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up SSL/HTTPS certificate
- [ ] Configure firewall rules
- [ ] Set up backups
- [ ] Configure logging/monitoring

---

## 📞 Troubleshooting

### Port 8000 In Use
Change port in docker-compose.dev.yml:
```yml
ports:
  - "8001:8000"  # Use 8001 instead
```

### Database Connection Error
Wait longer for DB to start:
```bash
sleep 15  # Linux/Mac
timeout /t 15  # Windows
```

### Permission Denied
Make scripts executable:
```bash
chmod +x *.sh
```

### Static Files Not Loading
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput
```

### Need Fresh Database
```bash
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
```

---

## 📚 Documentation Map

```
START HERE → SUMMARY.md
           ↓
QUICK SETUP → QUICKSTART.md
           ↓
FULL GUIDE → README.md
           ↓
PROJECT DETAILS → PROJECT.md
           ↓
PRODUCTION → DEPLOYMENT.md
           ↓
FILE INDEX → INDEX.md
```

---

## 💡 Pro Tips

**Tip 1**: Use `docker-compose ps` to see container status

**Tip 2**: Check logs before asking for help: `docker-compose logs web`

**Tip 3**: Django shell is useful: `docker-compose exec web python manage.py shell`

**Tip 4**: Always backup database before migrations

**Tip 5**: Keep dependencies updated monthly

---

## 🎓 Learning Resources

### Built-in Features to Explore
1. **Django Admin** - Full customization
2. **Models** - Database design
3. **Views** - Request handling
4. **Templates** - HTML rendering
5. **Forms** - User input

### External Resources
- Django Docs: https://docs.djangoproject.com/
- Docker Docs: https://docs.docker.com/
- Bootstrap Docs: https://getbootstrap.com/docs/5.3/

---

## 📊 Quick Commands Cheatsheet

| Task | Command |
|------|---------|
| **Start dev** | `build-dev.bat` or `./build-dev.sh` |
| **Stop dev** | `docker-compose -f docker-compose.dev.yml down` |
| **Create user** | `./manage-cms.sh dev createsuperuser` |
| **View logs** | `docker-compose -f docker-compose.dev.yml logs -f web` |
| **Database shell** | `docker-compose -f docker-compose.dev.yml exec db psql -U cmsuser -d cmsdb` |
| **Django shell** | `./manage-cms.sh dev shell` |
| **Migrations** | `./migrate.sh dev make` then `./migrate.sh dev migrate` |
| **Static files** | `./manage-cms.sh dev staticfiles` |
| **Deploy prod** | `./build-prod.sh` or `build-prod.bat` |

---

## ✅ Project Components

✅ Django 5.0+ Web Framework
✅ PostgreSQL 16 Database
✅ Nginx Web Server
✅ Gunicorn App Server
✅ Docker Containerization
✅ Bootstrap 5 Frontend
✅ CMS Admin Interface
✅ REST API Ready
✅ Security Hardened
✅ Production Optimized

---

## 🎉 You're All Set!

**Start**: Read [SUMMARY.md](SUMMARY.md)
**Run**: Execute build script
**Create**: Start adding content via admin
**Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Questions?** Check the documentation files.
**Issues?** Review [README.md](README.md) troubleshooting.
**Production?** See [DEPLOYMENT.md](DEPLOYMENT.md).

**Happy CMS-ing!** 🚀
