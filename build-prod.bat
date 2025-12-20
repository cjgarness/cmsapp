@echo off
REM Build and deploy the Django CMS application in production mode (Windows)

echo ======================================
echo Django CMS - Production Build Script
echo ======================================

REM Check if .env file exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please create .env file with production settings.
    exit /b 1
)

REM Check if docker is installed
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Docker not found. Please install Docker Desktop.
    exit /b 1
)

where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Docker Compose not found. Please install Docker Desktop.
    exit /b 1
)

echo.
echo Pulling latest base images...
docker pull python:3.12-slim
docker pull postgres:16-alpine
docker pull nginx:alpine

echo.
echo Building production Docker images...
docker-compose -f docker-compose.prod.yml build --no-cache

echo.
echo Starting production services...
docker-compose -f docker-compose.prod.yml up -d

echo.
echo Waiting for database to be ready...
timeout /t 15

echo.
echo Running database migrations...
docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate

echo.
echo Collecting static files...
docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput

echo.
echo ======================================
echo Production deployment successful!
echo ======================================
echo.
echo Access the application at: http://localhost
echo Access admin panel at: http://localhost/admin
echo.
echo Useful commands:
echo   - View logs: docker-compose -f docker-compose.prod.yml logs -f
echo   - Create superuser: docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
echo   - Stop services: docker-compose -f docker-compose.prod.yml down
echo   - Restart services: docker-compose -f docker-compose.prod.yml restart
echo.
