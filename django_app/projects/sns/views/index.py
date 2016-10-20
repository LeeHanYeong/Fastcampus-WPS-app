from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from member.forms import LoginForm
User = get_user_model()

__all__ = [
    'index',
]

def index(request):
    return render(request, 'projects/sns/index.html', {})