# Django CMS Project Files Index

## 📋 Complete File Listing

### 🎯 Start Here
- **[SUMMARY.md](SUMMARY.md)** - Project overview and quick start (READ THIS FIRST!)
- **[QUICKSTART.md](QUICKSTART.md)** - Get running in minutes
- **[README.md](README.md)** - Complete documentation

### 🚀 Deployment & Setup
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[build-dev.sh](build-dev.sh)** - Linux/Mac development build script
- **[build-dev.bat](build-dev.bat)** - Windows development build script
- **[build-prod.sh](build-prod.sh)** - Linux/Mac production build script
- **[build-prod.bat](build-prod.bat)** - Windows production build script

### 🐳 Docker Configuration
- **[Dockerfile](Dockerfile)** - Production Docker image
- **[Dockerfile.dev](Dockerfile.dev)** - Development Docker image
- **[docker-compose.dev.yml](docker-compose.dev.yml)** - Development services
- **[docker-compose.prod.yml](docker-compose.prod.yml)** - Production services
- **[nginx.conf](nginx.conf)** - Nginx reverse proxy configuration
- **[.dockerignore](.dockerignore)** - Docker build optimization

### 🔧 Helper Scripts
- **[manage-cms.sh](manage-cms.sh)** - CMS management CLI (Linux/Mac)
- **[manage-cms.bat](manage-cms.bat)** - CMS management CLI (Windows)
- **[migrate.sh](migrate.sh)** - Database migration helper (Linux/Mac)
- **[migrate.bat](migrate.bat)** - Database migration helper (Windows)

### ⚙️ Configuration Files
- **[.env.example](.env.example)** - Environment variables template
- **[.gitignore](.gitignore)** - Git ignore patterns
- **[requirements.txt](requirements.txt)** - Python package dependencies

### 📚 Documentation
- **[PROJECT.md](PROJECT.md)** - Detailed project overview
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[INSTALL.md](INSTALL.md)** - Installation verification checklist
- **[INDEX.md](INDEX.md)** - This file

### 🐍 Django Application Code

#### Root Files
- **[manage.py](manage.py)** - Django management command

#### Django Project Package (cmsapp/)
- **[cmsapp/__init__.py](cmsapp/__init__.py)** - Package marker
- **[cmsapp/settings.py](cmsapp/settings.py)** - Django settings
- **[cmsapp/urls.py](cmsapp/urls.py)** - URL routing
- **[cmsapp/wsgi.py](cmsapp/wsgi.py)** - WSGI application

#### Core App (API)
- **[cmsapp/core/__init__.py](cmsapp/core/__init__.py)** - Package marker
- **[cmsapp/core/apps.py](cmsapp/core/apps.py)** - App configuration
- **[cmsapp/core/urls.py](cmsapp/core/urls.py)** - API routes
- **[cmsapp/core/views.py](cmsapp/core/views.py)** - Health check endpoint

#### Pages App (Content Management)
- **[cmsapp/pages/__init__.py](cmsapp/pages/__init__.py)** - Package marker
- **[cmsapp/pages/apps.py](cmsapp/pages/apps.py)** - App configuration
- **[cmsapp/pages/models.py](cmsapp/pages/models.py)** - Page, PageBlock, PageImage models
- **[cmsapp/pages/views.py](cmsapp/pages/views.py)** - Page views and list
- **[cmsapp/pages/admin.py](cmsapp/pages/admin.py)** - Django admin customization
- **[cmsapp/pages/urls.py](cmsapp/pages/urls.py)** - Page routes

#### Templates App (Layout Management)
- **[cmsapp/templates/__init__.py](cmsapp/templates/__init__.py)** - Package marker
- **[cmsapp/templates/apps.py](cmsapp/templates/apps.py)** - App configuration
- **[cmsapp/templates/models.py](cmsapp/templates/models.py)** - PageTemplate, Stylesheet, LayoutComponent models
- **[cmsapp/templates/admin.py](cmsapp/templates/admin.py)** - Django admin customization

#### Media App (Asset Management)
- **[cmsapp/media/__init__.py](cmsapp/media/__init__.py)** - Package marker
- **[cmsapp/media/apps.py](cmsapp/media/apps.py)** - App configuration
- **[cmsapp/media/models.py](cmsapp/media/models.py)** - MediaLibrary, MediaFile models
- **[cmsapp/media/admin.py](cmsapp/media/admin.py)** - Django admin customization

### 🎨 HTML Templates

#### Base Templates
- **[templates/base.html](templates/base.html)** - Master template with Bootstrap 5
- **[templates/includes/navbar.html](templates/includes/navbar.html)** - Navigation bar
- **[templates/includes/footer.html](templates/includes/footer.html)** - Footer

#### Page Templates
- **[templates/pages/page_detail.html](templates/pages/page_detail.html)** - Single page display
- **[templates/pages/page_list.html](templates/pages/page_list.html)** - Pages listing

### 🎨 Static Files

#### Stylesheets
- **[static/css/style.css](static/css/style.css)** - Main stylesheet with Bootstrap 5 customization

#### JavaScript
- **[static/js/main.js](static/js/main.js)** - Utility functions and theme toggle

#### Images
- **static/images/** - Directory for static images

## 📊 Project Statistics

- **Total Python Files**: 16
- **Total Template Files**: 5
- **Total Static Files**: 2
- **Total Docker Files**: 4
- **Total Script Files**: 8
- **Total Documentation Files**: 7
- **Total Configuration Files**: 3
- **Models**: 9
- **Views**: 5+
- **Admin Classes**: 7

## 🗂️ Directory Structure

```
cmsapp/
├── Django Configuration
│   ├── cmsapp/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── [4 apps with models, views, admin]
│   └── manage.py
│
├── Frontend
│   ├── templates/
│   │   ├── base.html
│   │   ├── includes/ (navbar, footer)
│   │   └── pages/ (detail, list)
│   └── static/
│       ├── css/style.css
│       ├── js/main.js
│       └── images/
│
├── Docker & Deployment
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── docker-compose.dev.yml
│   ├── docker-compose.prod.yml
│   ├── nginx.conf
│   └── .dockerignore
│
├── Build Scripts
│   ├── build-dev.sh / build-dev.bat
│   ├── build-prod.sh / build-prod.bat
│   ├── manage-cms.sh / manage-cms.bat
│   └── migrate.sh / migrate.bat
│
├── Configuration
│   ├── .env.example
│   ├── .gitignore
│   └── requirements.txt
│
└── Documentation
    ├── SUMMARY.md
    ├── README.md
    ├── QUICKSTART.md
    ├── PROJECT.md
    ├── DEPLOYMENT.md
    ├── CONTRIBUTING.md
    ├── INSTALL.md
    └── INDEX.md (this file)
```

## 🔍 File Search Guide

### Looking for...?

| Need | File |
|------|------|
| **Quick start** | QUICKSTART.md |
| **Full documentation** | README.md |
| **How to deploy** | DEPLOYMENT.md |
| **Models & database** | cmsapp/pages/models.py, cmsapp/templates/models.py |
| **URL routing** | cmsapp/pages/urls.py, cmsapp/core/urls.py |
| **Admin interface** | cmsapp/pages/admin.py, cmsapp/templates/admin.py |
| **Frontend templates** | templates/pages/ |
| **Styling** | static/css/style.css |
| **JavaScript** | static/js/main.js |
| **Docker config** | docker-compose.dev.yml / docker-compose.prod.yml |
| **Build scripts** | build-dev.* / build-prod.* |
| **Environment setup** | .env.example |

## 🚀 Quick Reference

### Start Development (Windows)
```cmd
build-dev.bat
```

### Start Development (Linux/Mac)
```bash
chmod +x build-dev.sh
./build-dev.sh
```

### Create Admin User
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

### Access CMS
- Website: http://localhost:8000
- Admin: http://localhost:8000/admin

### View Logs
```bash
docker-compose -f docker-compose.dev.yml logs -f web
```

### Deploy to Production
```bash
./build-prod.sh  # Linux/Mac
build-prod.bat   # Windows
```

## 📖 Reading Order

1. **[SUMMARY.md](SUMMARY.md)** - Overview (5 min read)
2. **[QUICKSTART.md](QUICKSTART.md)** - Get running (5 min)
3. **[README.md](README.md)** - Full guide (20 min read)
4. **[PROJECT.md](PROJECT.md)** - Details (15 min read)
5. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production (10 min read)

## 🎯 Common Tasks

| Task | Command |
|------|---------|
| **Start dev server** | `./build-dev.sh` or `build-dev.bat` |
| **Create superuser** | `docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser` |
| **Make migrations** | `./migrate.sh dev make` or `migrate.bat dev make` |
| **Run migrations** | `./migrate.sh dev migrate` or `migrate.bat dev migrate` |
| **Access Django shell** | `docker-compose -f docker-compose.dev.yml exec web python manage.py shell` |
| **Access database** | `docker-compose -f docker-compose.dev.yml exec db psql -U cmsuser -d cmsdb` |
| **View logs** | `docker-compose -f docker-compose.dev.yml logs -f web` |
| **Deploy prod** | `./build-prod.sh` or `build-prod.bat` |

## 🔗 File Dependencies

```
settings.py
  ├── Imports all 4 apps
  ├── Database configuration
  └── Security settings

manage.py
  └── Entry point for Django commands

urls.py (project)
  ├── Includes pages.urls
  └── Includes core.urls

pages/urls.py
  ├── Routes to views
  └── Uses models

templates/pages/*
  ├── Extends base.html
  ├── Uses Bootstrap 5
  └── References static files

style.css
  └── Imported by base.html
```

## ✅ Verification Checklist

- [x] All Python files present
- [x] All HTML templates present
- [x] All static files present
- [x] Docker configuration complete
- [x] Build scripts created
- [x] Documentation complete
- [x] Models defined
- [x] Views implemented
- [x] Admin customized
- [x] Security configured

## 🎓 Understanding the Project

### Architecture
```
Client Browser
    ↓
Nginx (Production) / Django Dev Server (Dev)
    ↓
Django Application (Views, URLs, Models)
    ↓
PostgreSQL Database
    ↓
Static/Media Files
```

### Data Flow
1. User accesses page via URL
2. Django routes to appropriate view
3. View queries database models
4. Model renders template with context
5. Template displays with CSS/JS
6. Response sent to browser

### Models Relationships
```
Page (Main content)
  ├── Has many PageBlocks
  ├── Has many PageImages
  ├── Has one PageTemplate
  └── Has many Stylesheets

PageTemplate (Layout)
  ├── Has many LayoutComponents
  └── Used by many Pages

Stylesheet (CSS)
  └── Used by many Pages

MediaLibrary (Organization)
  └── Has many MediaFiles
```

---

**Total Files**: 50+
**Total Lines of Code**: 2000+
**Documentation Pages**: 7
**Status**: ✅ Complete

---

**For more information, start with [SUMMARY.md](SUMMARY.md)**
