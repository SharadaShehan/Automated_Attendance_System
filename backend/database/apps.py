from django.apps import AppConfig
import os

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return True

        # Import scheduler and the command
        from apscheduler.schedulers.background import BackgroundScheduler
        from database.management.commands.delete_expired_tokens import Command

        # Create a scheduler instance
        scheduler = BackgroundScheduler()

        scheduler.add_job(Command().handle, 'interval', hours=2)

        # Start the scheduler
        scheduler.start()
