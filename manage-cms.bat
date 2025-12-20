@echo off
REM Helper script to manage the CMS application on Windows

setlocal enabledelayedexpansion

set ENVIRONMENT=%1
set COMMAND=%2

if "!ENVIRONMENT!"=="" (
    set ENVIRONMENT=dev
)

if "!ENVIRONMENT!"!="dev" if "!ENVIRONMENT!"!="prod" (
    echo Usage: manage-cms.bat [dev^|prod] [command]
    echo.
    echo Commands:
    echo   createsuperuser - Create a Django superuser
    echo   shell           - Open Django shell
    echo   dbshell         - Open database shell
    echo   clearcache      - Clear all caches
    echo   staticfiles     - Collect static files
    echo   help            - Show Django help
    exit /b 1
)

set COMPOSE_FILE=docker-compose.!ENVIRONMENT!.yml
set COMPOSE_CMD=docker-compose -f !COMPOSE_FILE!

if "!COMMAND!"=="createsuperuser" (
    !COMPOSE_CMD! exec web python manage.py createsuperuser
) else if "!COMMAND!"=="shell" (
    !COMPOSE_CMD! exec web python manage.py shell
) else if "!COMMAND!"=="dbshell" (
    !COMPOSE_CMD! exec db psql -U cmsuser -d cmsdb
) else if "!COMMAND!"=="clearcache" (
    echo Clearing cache...
    !COMPOSE_CMD! exec web python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('Cache cleared')"
) else if "!COMMAND!"=="staticfiles" (
    echo Collecting static files...
    !COMPOSE_CMD! exec web python manage.py collectstatic --noinput
) else if "!COMMAND!"=="help" (
    !COMPOSE_CMD! exec web python manage.py help
) else (
    echo Running: python manage.py !COMMAND!
    !COMPOSE_CMD! exec web python manage.py !COMMAND!
)
