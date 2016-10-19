from django.core.management.base import BaseCommand
from member.models import MyUser as User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(email='lhy@lhy.kr').exists():
            User.objects.create_superuser(email='lhy@lhy.kr', password='dlgksdud1')