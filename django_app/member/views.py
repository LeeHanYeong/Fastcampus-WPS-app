import requests
import json
from urllib.parse import quote
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.views.generic import TemplateView

from apis import facebook
from member.forms import LoginForm
User = get_user_model()


def login1(request):
    login_next = request.GET.get('next')
    if request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
        except KeyError:
            return HttpResponse('email 또는 password는 필수항목입니다')

        user = authenticate(
            email=email,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, '로그인 되었습니다')
            if login_next:
                return redirect(login_next)
            return redirect('blog:post_list')
        else:
            messages.error(request, '로그인에 실패했습니다')
            return redirect('member:login')
    else:
        context = {
            'next': login_next,
        }
        return render(request, 'member/login.html', context)


class Login(TemplateView, FormView):
    form_class = LoginForm
    template_name = 'member/login2.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(email=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return HttpResponse('ID/PW 오류')



def login2(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)

    else:
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'member/login2.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, '로그아웃 되었습니다')
    return redirect('blog:post_list')


def login_facebook(request):
    login_next = request.GET.get('login_next')
    # quote_login_next = quote(login_next, safe='')
    # quote_login_next = login_next
    # print('login_next : %s' % login_next)
    # print('quote_login_next : %s' % quote_login_next)
    REDIRECT_URI = '{}{}'.format('%s://%s' % (request.scheme, request.META['HTTP_HOST']), reverse('member:login_facebook'))

    if request.GET.get('error'):
        messages.error(request, '사용자에 의해 페이스북 로그인 거부')
        return redirect('member:login')

    if request.GET.get('code'):
        code = request.GET.get('code')
        print('code: %s' % code)

        access_token = facebook.get_access_token(code, REDIRECT_URI)
        user_id = facebook.get_user_id_from_access_token(access_token)
        user_info = facebook.get_user_info(user_id, access_token)

        user = authenticate(user_info=user_info)
        if user is not None:
            login(request, user)
            messages.success(request, '페이스북 아이디로 로그인 되었습니다')
            if login_next:
                return redirect(login_next)
            else:
                return redirect('blog:post_list')
        else:
            messages.error(request, '페이스북 로그인에 실패하였습니다')
            return redirect('member:login')
