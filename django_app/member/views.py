import requests
import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from member.forms import LoginForm
# https://docs.djangoproject.com/en/1.10/
# topics/auth/default/#auth-web-requests


@csrf_exempt
def login1(request):
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
            messages.success(request, '로그아웃 되었습니다')
            return redirect('blog:post_list')
        else:
            messages.error(request, '로그인에 실패했습니다')
            return redirect('member:login')
    else:
        return render(request, 'member/login.html', {})


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
    APP_ID = '687819251371707'
    SECRET_ID = '2481784215fed90a8dc8ecfc7b572196'
    APP_ACCESS_TOKEN = '%s|%s' % (APP_ID, SECRET_ID)
    URL_LOGIN_FACEBOOK = '{}{}'.format('http://localhost:8081', reverse('member:login_facebook'))

    if request.GET.get('error'):
        return HttpResponse('사용자에 의해 거부')
    if request.GET.get('code'):
        code = request.GET.get('code')
        url_request_access_token = 'https://graph.facebook.com/v2.3/oauth/access_token?client_id={}&redirect_uri={}&client_secret={}&code={}'.format(
            APP_ID, URL_LOGIN_FACEBOOK, SECRET_ID, code)
        r = requests.get(url_request_access_token)
        dict_access_token = r.json()
        access_token = dict_access_token.get('access_token')

        url_request_user_id = 'https://graph.facebook.com/debug_token?input_token={it}&access_token={at}'.format(
            it=access_token, at=APP_ACCESS_TOKEN
        )
        r = requests.get(url_request_user_id)
        dict_user_id = r.json()
        print(dict_user_id)
        user_id = dict_user_id['data'].get('user_id')

        url_request_user_info = 'https://graph.facebook.com/{uid}?fields=id,name,first_name,last_name,age_range,link,gender,locale,picture,timezone,updated_time,verified,email&access_token={access_token}'.format(
            uid=user_id, access_token=access_token
        )
        r = requests.get(url_request_user_info)
        dict_user_info = r.json()
        print(dict_user_info)

        ret = 'AccessToken : {at}<br>Code : {code}<br>UserID : {user_id}'.format(
            at=access_token,
            code=code,
            user_id=user_id
        )
        return HttpResponse(ret)