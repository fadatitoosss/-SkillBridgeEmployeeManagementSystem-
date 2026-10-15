"""
Create a superuser from environment variables if one doesn't exist yet.
Used on Render's free tier because Shell access is not available.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create a superuser from environment variables if none exists."

    def handle(self, *args, **kwargs):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        if not username or not password:
            self.stdout.write(self.style.WARNING(
                "DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set. Skipping."
            ))
            return
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already exists."))
            return
        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))