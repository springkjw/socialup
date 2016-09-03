from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(email="springkjw@gmail.com").exists():
            User.objects.create_superuser("springkjw@gmail.com", "wodnjs2010")