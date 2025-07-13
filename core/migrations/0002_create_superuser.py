# core/migrations/0002_create_superuser.py

from django.db import migrations
from django.conf import settings
import os

def create_superuser(apps, schema_editor):
    """
    Creates the default superuser for the site using environment variables.
    """
    User = apps.get_model(settings.AUTH_USER_MODEL)

    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'complexpassword123')

    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print(f"Superuser '{username}' already exists. Skipping creation.")


class Migration(migrations.Migration):

    dependencies = [
        # CORRECTED: This now depends on the last migration of your 'accounts' app.
        # This ensures the User and Profile tables exist before we try to create a superuser.
        ('accounts', '0004_remove_profile_profile_picture_and_more'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]