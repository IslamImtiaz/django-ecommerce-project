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


# In core/migrations/0002_create_superuser.py

class Migration(migrations.Migration):

    # This line tells Django that this migration depends on the first migration of the 'core' app
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]