from django.apps import AppConfig
from datetime import datetime, timedelta
import os

class MiddlewareApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'middleware_api'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return True

        # Import scheduler and the command
        from apscheduler.schedulers.background import BackgroundScheduler
        from middleware_api.management.commands.start_ml_model import Command

        # Create a scheduler instance
        scheduler = BackgroundScheduler()

        # Add the job with max_instances=1 to ensure it runs only once
        time_to_run = datetime.now()+timedelta(seconds=3)
        scheduler.add_job(Command().handle, 'date', run_date=time_to_run, args=[], id='my_unique_job_id', max_instances=1)

        scheduler.start()

