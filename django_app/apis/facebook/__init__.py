from django.conf import settings
APP_ID = settings.FACEBOOK_APP_ID
SECRET_CODE = settings.FACEBOOK_SECRET_CODE
APP_ACCESS_TOKEN = settings.FACEBOOK_APP_ACCESS_TOKEN

from .token import get_access_token, get_user_info, get_user_id_from_access_token