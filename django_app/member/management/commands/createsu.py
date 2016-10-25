import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from member.models import MyUser as User
CONF_DIR = settings.CONF_DIR
config = json.loads(open(os.path.join(CONF_DIR, 'settings_debug.json')).read())


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = config['defaultSuperuser']['email']
        password = config['defaultSuperuser']['password']
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password)
            print('default superuser created')
        else:
            print('default superuser exist')