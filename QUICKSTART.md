# CMS Quick Start Guide

Get the CMS running in minutes!

## For Windows Users

### 1. Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Git (optional, for cloning)

### 2. Quick Start

```cmd
# Open PowerShell/Command Prompt and navigate to project
cd path\to\cmsapp

# Run development build
build-dev.bat

# Wait for services to start (about 2-3 minutes)
```

### 3. Access the CMS

- **Website**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Create Admin Account**:
```cmd
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

### 4. Stop Services

```cmd
docker-compose -f docker-compose.dev.yml down
```

---

## For Linux/Mac Users

### 1. Prerequisites
- Docker Desktop or Docker + Docker Compose
- Git (optional)

### 2. Quick Start

```bash
# Navigate to project
cd /path/to/cmsapp

# Make scripts executable
chmod +x build-dev.sh

# Run development build
./build-dev.sh

# Wait for services to start
```

### 3. Access the CMS

- **Website**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Create Admin Account**:
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

### 4. Stop Services

```bash
docker-compose -f docker-compose.dev.yml down
```

---

## Common Tasks

### Create Your First Page

1. Go to http://localhost:8000/admin
2. Login with your superuser credentials
3. Click "Pages" > "Add Page"
4. Fill in:
   - Title: "Welcome"
   - Description: "Welcome to our CMS"
   - Content: "Hello World!"
   - Status: "Published"
   - Check "Is homepage"
5. Save and visit http://localhost:8000

### Upload an Image

1. Go to Admin > Media > Media Files
2. Click "Add Media File"
3. Select a file
4. Fill in title and description
5. Save

### Create a Custom Template

1. Go to Admin > Templates > Page Templates
2. Click "Add Page Template"
3. Upload an HTML template file
4. Set layout type
5. Pages can now use this template

### Customize Stylesheets

1. Go to Admin > Templates > Stylesheets
2. Click "Add Stylesheet"
3. Upload a CSS file
4. Mark as active
5. Pages can link to this stylesheet

---

## Docker Commands Reference

```bash
# View running containers
docker-compose -f docker-compose.dev.yml ps

# View logs
docker-compose -f docker-compose.dev.yml logs -f web

# Execute commands
docker-compose -f docker-compose.dev.yml exec web python manage.py <command>

# Access database
docker-compose -f docker-compose.dev.yml exec db psql -U cmsuser -d cmsdb

# Rebuild containers
docker-compose -f docker-compose.dev.yml build --no-cache
```

---

## Troubleshooting

### Port 8000 Already in Use
```bash
# Change port in docker-compose.dev.yml:
# ports:
#   - "8001:8000"  # Use 8001 instead
```

### Database Connection Error
```bash
# Wait a bit longer and retry - database takes time to start
docker-compose -f docker-compose.dev.yml logs db
```

### Permission Denied
```bash
# Make scripts executable
chmod +x build-dev.sh build-prod.sh
```

---

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Visit [Admin Panel](http://localhost:8000/admin) to manage content

**Need Help?** Check the troubleshooting section in [README.md](README.md)

---

**CMS Version**: 1.0.0  
**Django Version**: 5.0+  
**Python Version**: 3.12+
