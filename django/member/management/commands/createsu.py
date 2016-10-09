from django.core.management.base import BaseCommand
from member.models import FastcampusUser as User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='lhy').exists():
            User.objects.create_superuser(username='lhy', password='gksdud27')