@echo off
REM Build and run the Django CMS application in development mode (Windows)

echo ======================================
echo Django CMS - Development Build Script
echo ======================================

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo .env file created. Please update it with your settings.
)

REM Check if docker is installed
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo Docker not found. Please install Docker Desktop.
    exit /b 1
)

where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo Docker Compose not found. Please install Docker Desktop.
    exit /b 1
)

echo.
echo Pulling latest base images...
docker pull python:3.12-slim
docker pull postgres:16-alpine

echo.
echo Building Docker images for development...
docker-compose -f docker-compose.dev.yml build --no-cache

echo.
echo Starting development services...
docker-compose -f docker-compose.dev.yml up -d

echo.
echo Waiting for database to be ready...
timeout /t 10

echo.
echo Running migrations...
docker-compose -f docker-compose.dev.yml exec -T web python manage.py migrate

echo.
echo Collecting static files...
docker-compose -f docker-compose.dev.yml exec -T web python manage.py collectstatic --noinput

echo.
echo ======================================
echo Development environment ready!
echo ======================================
echo.
echo Access the application at: http://localhost:8000
echo Access admin panel at: http://localhost:8000/admin
echo.
echo Useful commands:
echo   - View logs: docker-compose -f docker-compose.dev.yml logs -f web
echo   - Create superuser: docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
echo   - Stop services: docker-compose -f docker-compose.dev.yml down
echo   - Shell: docker-compose -f docker-compose.dev.yml exec web python manage.py shell
echo.
