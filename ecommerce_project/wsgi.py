"""
WSGI config for ecommerce_project project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')

# Get the standard Django application
application = get_wsgi_application()

# If in production, wrap the application with WhiteNoise to serve static AND media files
if not settings.DEBUG:
    application = WhiteNoise(application, root=settings.STATIC_ROOT)
    application.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)