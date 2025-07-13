# core/apps.py
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        This method is called once Django is ready.
        We'll start our background scheduler here.
        """
        from . import jobs
        jobs.start()