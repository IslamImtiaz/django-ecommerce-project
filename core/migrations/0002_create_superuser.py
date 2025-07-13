# core/migrations/0002_create_superuser.py (or your file number)

from django.db import migrations
from django.conf import settings
import os

def create_superuser(apps, schema_editor):
    """
    Creates the default superuser and their associated Profile.
    """
    User = apps.get_model(settings.AUTH_USER_MODEL)
    # We need to get the Profile model from the 'accounts' app
    Profile = apps.get_model('accounts', 'Profile')

    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'complexpassword123')

    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}")
        # Create the user
        user = User.objects.create_superuser(username=username, email=email, password=password)

        # NEW: Explicitly create a Profile for the new superuser
        Profile.objects.create(user=user)
        print(f"Profile created for superuser: {username}")
    else:
        print(f"Superuser '{username}' already exists. Skipping creation.")


class Migration(migrations.Migration):
    dependencies = [
        # Ensure this depends on your last 'accounts' migration where the Profile model exists
        ('accounts', '0004_remove_profile_profile_picture_and_more'),
    ]
    operations = [
        migrations.RunPython(create_superuser),
    ]