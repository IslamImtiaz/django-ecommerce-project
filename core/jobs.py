# core/jobs.py
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.management import call_command
import sys
import os # Import the os module

def update_rates_job():
    """
    This is the function that will be scheduled.
    It runs the 'update_rates' management command.
    """
    try:
        call_command('update_rates')
        print("Successfully executed 'update_rates' scheduled job.")
    except Exception as e:
        print(f"Error running 'update_rates' scheduled job: {e}")

def start():
    """
    The main function to start the scheduler.
    """
    # This check prevents the scheduler from running in the main process
    # of the development server's reloader, solving the "double run" issue.
    if os.environ.get('RUN_MAIN') == 'true' or 'runserver' not in sys.argv:
        return

    print("Starting currency update scheduler...") # This will now only print once
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        update_rates_job,
        trigger='interval',
        hours=12,
        id='update_rates_job',
        jobstore='default',
        replace_existing=True,
    )

    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
    except Exception as e:
        print(f"Scheduler failed to start: {e}")