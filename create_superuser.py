"""
Script to create a Django superuser if one doesn't exist.
Uses environment variables for superuser credentials.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmsapp.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser "{username}" created successfully.')
else:
    print(f'Superuser "{username}" already exists.')
