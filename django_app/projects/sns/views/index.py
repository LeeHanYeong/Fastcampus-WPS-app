from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.conf import settings

User = get_user_model()

__all__ = [
    'index',
]

def index(request):
    context = {
        'facebook_app_id': settings.FACEBOOK_APP_ID,
    }
    return render(request, 'projects/sns/index.html', context)