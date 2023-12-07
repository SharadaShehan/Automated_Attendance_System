from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Delete expired tokens'

    def handle(self, *args, **options):
        now = timezone.now()  # Use timezone-aware datetime object
        expired_tokens = Token.objects.filter(created__lt=now - timezone.timedelta(hours=24))
        for token in expired_tokens:
            token.delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted expired tokens.'))
