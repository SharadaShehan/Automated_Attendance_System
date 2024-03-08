from django.core.management.base import BaseCommand
from middleware_api.ml_model import MLModel


class Command(BaseCommand):
    help = 'Starts the ML model when the Django project starts'

    def handle(self, *args, **options):
        MLModel.start_ml_model()
