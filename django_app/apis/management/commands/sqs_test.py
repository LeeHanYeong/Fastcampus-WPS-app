import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from apis.mail.asdf import asdfasdf
CONF_DIR = settings.CONF_DIR
config = json.loads(open(os.path.join(CONF_DIR, 'settings_debug.json')).read())


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('===SqsMailTest Start===')
        asdfasdf.delay()
        print('===SqsMailTest End===')