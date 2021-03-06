import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from apis.mail import send_test
CONF_DIR = settings.CONF_DIR
config = json.loads(open(os.path.join(CONF_DIR, 'settings_debug.json')).read())


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('===SendMailTest Start===')
        send_test()
        print('===SendMailTest End===')