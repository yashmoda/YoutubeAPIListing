from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from search_video.models import APIKeys


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.filter(username="admin").count() == 0:
            admin = User.objects.create_superuser("admin", "test@gmail.com", "admin")
            admin.is_admin = True
            admin.is_active = True
            admin.save()
            for key in API_KEYS:
                APIKeys(api_key=key).save()
        return
