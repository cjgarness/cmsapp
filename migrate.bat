@echo off
REM Database migration helper script for Windows

setlocal enabledelayedexpansion

set ENVIRONMENT=%1
if "!ENVIRONMENT!"=="" set ENVIRONMENT=dev

if "!ENVIRONMENT!"=="dev" (
    set COMPOSE_FILE=docker-compose.dev.yml
    set COMPOSE_CMD=docker-compose -f !COMPOSE_FILE!
) else if "!ENVIRONMENT!"=="prod" (
    set COMPOSE_FILE=docker-compose.prod.yml
    set COMPOSE_CMD=docker-compose -f !COMPOSE_FILE!
) else (
    echo Usage: migrate.bat [dev^|prod] [make^|migrate^|show]
    exit /b 1
)

set COMMAND=%2

if "!COMMAND!"=="make" (
    echo Creating migrations...
    !COMPOSE_CMD! exec web python manage.py makemigrations core media pages templates
) else if "!COMMAND!"=="migrate" (
    echo Applying migrations...
    !COMPOSE_CMD! exec web python manage.py migrate
) else if "!COMMAND!"=="show" (
    echo Migration status...
    !COMPOSE_CMD! exec web python manage.py showmigrations
) else (
    echo Usage: migrate.bat [dev^|prod] [make^|migrate^|show]
    exit /b 1
)
