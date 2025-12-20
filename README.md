# Django 5 Content Management System

A modern, fully containerized Django 5 based content management system with support for customizable page layouts, templates, graphics, and stylesheets.

## Features

- **Django 5.0** - Latest Django framework
- **Customizable Page Layouts** - Multiple template options (single-column, two-column, three-column, hero, masonry, custom)
- **Media Management** - Centralized media library for images, videos, and documents
- **Page Blocks** - Reusable content blocks (text, images, galleries, videos, code, custom HTML)
- **Stylesheets** - Custom CSS stylesheets management
- **Template System** - Upload and manage Django templates
- **Responsive Design** - Bootstrap 5 integrated
- **Admin Interface** - Comprehensive Django admin customization
- **Docker Containerization** - Complete production and development environments
- **PostgreSQL** - Production-ready database
- **Nginx** - Production reverse proxy
- **Health Checks** - Built-in health monitoring
- **Logging** - Structured logging for debugging

## Project Structure

```
cmsapp/
├── cmsapp/                    # Django project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # URL routing
│   ├── wsgi.py               # WSGI configuration
│   ├── core/                 # Core app (API endpoints)
│   ├── pages/                # Pages app (CMS content)
│   ├── templates/            # Template management
│   └── media/                # Media management
├── templates/                # Project templates
│   ├── base.html            # Base template
│   ├── includes/            # Template includes
│   └── pages/               # Page templates
├── static/                   # Static files
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript
│   └── images/              # Static images
├── media/                    # User-uploaded media
├── manage.py               # Django management command
├── requirements.txt        # Python dependencies
├── Dockerfile             # Production Docker image
├── Dockerfile.dev         # Development Docker image
├── docker-compose.dev.yml # Development Docker Compose
├── docker-compose.prod.yml # Production Docker Compose
├── nginx.conf             # Nginx configuration
├── build-dev.sh          # Development build script (Linux/Mac)
├── build-dev.bat         # Development build script (Windows)
├── build-prod.sh         # Production build script (Linux/Mac)
├── build-prod.bat        # Production build script (Windows)
└── README.md            # This file
```

## System Requirements

### Local Development
- Docker Desktop (includes Docker and Docker Compose)
- Git (for version control)
- At least 2GB free disk space

### Production
- Docker and Docker Compose
- Linux server (Ubuntu 20.04+ recommended)
- 2GB+ RAM
- 20GB+ disk space
- SSL certificate (for HTTPS)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/cmsapp.git
cd cmsapp
```

### 2. Configure Environment

Copy the environment template and update with your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
DEBUG=True                          # Set to False in production
SECRET_KEY=your-secret-key-here    # Generate: python -c 'import secrets; print(secrets.token_urlsafe())'
ALLOWED_HOSTS=localhost,127.0.0.1  # Add your domain in production
DATABASE_NAME=cmsdb
DATABASE_USER=cmsuser
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 3. Development Setup (Linux/Mac)

```bash
chmod +x build-dev.sh
./build-dev.sh
```

### 3. Development Setup (Windows)

```cmd
build-dev.bat
```

### 4. Production Setup (Linux/Mac)

```bash
chmod +x build-prod.sh
./build-prod.sh
```

### 4. Production Setup (Windows)

```cmd
build-prod.bat
```

## Usage

### Development Server

The development server runs on `http://localhost:8000`

#### View Logs
```bash
docker-compose -f docker-compose.dev.yml logs -f web
```

#### Create Superuser
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

#### Access Django Shell
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py shell
```

#### Run Migrations
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
```

#### Collect Static Files
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput
```

### Production Server

The production server runs on `http://localhost` (port 80)

#### View Logs
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

#### Create Superuser
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

#### Restart Services
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Stop Services

#### Development
```bash
docker-compose -f docker-compose.dev.yml down
```

#### Production
```bash
docker-compose -f docker-compose.prod.yml down
```

## Models Overview

### Pages App
- **Page** - Main CMS page with title, content, status, template
- **PageBlock** - Reusable content blocks (text, image, gallery, etc.)
- **PageImage** - Image assets with metadata

### Templates App
- **PageTemplate** - Layout templates with different layout types
- **Stylesheet** - CSS files for customization
- **LayoutComponent** - Reusable layout components (header, footer, sidebar)

### Media App
- **MediaLibrary** - Organization container for media files
- **MediaFile** - Individual media files with metadata

## API Endpoints

### Health Check
```
GET /api/health/
```

Returns:
```json
{
  "status": "healthy",
  "service": "CMS API"
}
```

## Admin Interface

Access the admin panel at:
- Development: `http://localhost:8000/admin`
- Production: `http://localhost/admin`

Default superuser credentials are set during `createsuperuser` command.

## Docker Images

### Images Used
- `python:3.12-slim` - Latest Python runtime
- `postgres:16-alpine` - Latest PostgreSQL database
- `nginx:alpine` - Latest Nginx web server

All images are pulled from official repositories and updated automatically.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DEBUG | False | Enable debug mode |
| SECRET_KEY | - | Django secret key |
| ALLOWED_HOSTS | localhost,127.0.0.1 | Allowed hostnames |
| DATABASE_NAME | cmsdb | PostgreSQL database name |
| DATABASE_USER | cmsuser | PostgreSQL user |
| DATABASE_PASSWORD | cmspass | PostgreSQL password |
| DATABASE_HOST | db | PostgreSQL host |
| DATABASE_PORT | 5432 | PostgreSQL port |
| DJANGO_SETTINGS_MODULE | cmsapp.settings | Django settings module |
| CORS_ALLOWED_ORIGINS | http://localhost:3000 | CORS allowed origins |

## Security Considerations

### Development
- `DEBUG=True` is safe for local development only
- `SECRET_KEY` should be changed
- Use SQLite database for testing

### Production
- Set `DEBUG=False`
- Generate a strong `SECRET_KEY`
- Use `DATABASE_PASSWORD` with strong credentials
- Configure `ALLOWED_HOSTS` with your domain
- Enable HTTPS with SSL certificate
- Use environment variables for secrets (not in code)
- Regularly update Docker images
- Monitor application logs

## Database Migrations

### Create New Migration
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py makemigrations
```

### Apply Migrations
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
```

### View Migration Status
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py showmigrations
```

## Static Files & Media

### Static Files
Located in `./static/` and served by Nginx. Update with:
```bash
docker-compose -f docker-compose.[dev|prod].yml exec web python manage.py collectstatic --noinput
```

### Media Files
User-uploaded files stored in `./media/` directory. Ensure proper permissions:
```bash
chmod -R 755 media/
```

## Creating Custom Templates

1. Create an HTML template in `templates/` directory
2. Use Django template syntax with Bootstrap 5
3. Reference `base.html` for consistent styling
4. Upload via admin panel or place in `media/templates/`

## Customizing Stylesheets

1. Create CSS file in `static/css/` or `media/stylesheets/`
2. Reference Bootstrap 5 classes
3. Use CSS variables defined in `style.css`
4. Upload via media library in admin

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Connection Error
```bash
# Check database status
docker-compose -f docker-compose.dev.yml ps db

# View database logs
docker-compose -f docker-compose.dev.yml logs db
```

### Permission Denied on Scripts
```bash
# Make scripts executable
chmod +x build-dev.sh build-prod.sh
```

### Static Files Not Loading
```bash
# Collect static files
docker-compose -f docker-compose.[dev|prod].yml exec web python manage.py collectstatic --noinput

# Clear Nginx cache
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload
```

## Performance Optimization

### Caching
- Static files cached for 30 days
- Media files cached for 7 days
- Nginx configured with Gzip compression

### Database
- Use PostgreSQL indexes on frequently queried fields
- Implement query optimization in views
- Use select_related() and prefetch_related() for queries

### Application
- Use Gunicorn workers (default: 4)
- Implement Django cache framework
- Use CDN for static files in production

## Backup & Recovery

### Database Backup
```bash
docker-compose -f docker-compose.prod.yml exec db pg_dump -U cmsuser cmsdb > backup.sql
```

### Database Restore
```bash
docker-compose -f docker-compose.prod.yml exec -T db psql -U cmsuser cmsdb < backup.sql
```

### Media Backup
```bash
tar -czf media_backup.tar.gz media/
```

## Deployment to Production

1. **Prepare Server**: Install Docker and Docker Compose
2. **Configure .env**: Update all production settings
3. **Run Build Script**: Execute `build-prod.sh` or `build-prod.bat`
4. **Setup SSL**: Configure certificate with Nginx
5. **Monitor**: Set up logging and monitoring
6. **Backup**: Configure automated backups

## License

This project is open source and available under the MIT License.

## Support & Contribution

For issues, feature requests, or contributions, please visit the GitHub repository.

## Changelog

### Version 1.0.0 (Initial Release)
- Django 5.0 setup
- Complete CMS models
- Docker containerization
- Build scripts for dev/prod
- Responsive Bootstrap 5 templates
- Admin interface customization
- Static and media file handling

## Future Roadmap

- [ ] REST API endpoints
- [ ] GraphQL support
- [ ] User comments system
- [ ] Search functionality
- [ ] SEO optimization
- [ ] Content versioning
- [ ] Workflow management
- [ ] Analytics integration
- [ ] Multi-language support
- [ ] Cache layer (Redis)

---

**Last Updated**: December 2025
**Maintainer**: Your Name/Organization
