import requests
import json
from urllib.parse import quote
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from member.forms import LoginForm
User = get_user_model()


def login1(request):
    login_next = request.GET.get('login_next')
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
            'login_next': login_next,
        }
        return render(request, 'member/login.html', context)


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
    APP_ID = '338774269808826'
    SECRET_ID = 'b780a89551228b4c1015c529a7667722'
    APP_ACCESS_TOKEN = '%s|%s' % (APP_ID, SECRET_ID)
    URL_LOGIN_FACEBOOK = '{}{}'.format('http://%s' % request.META['HTTP_HOST'], reverse('member:login_facebook'))

    # if login_next:
    #     URL_LOGIN_FACEBOOK = '%s?login_next=%s' % (URL_LOGIN_FACEBOOK, quote_login_next)

    print('URL_LOGIN_FACEBOOK : %s' % URL_LOGIN_FACEBOOK)
    if request.GET.get('error'):
        messages.error(request, '사용자에 의해 페이스북 로그인 거부')
        return redirect('member:login')

    if request.GET.get('code'):
        code = request.GET.get('code')
        print('code: %s' % code)
        url_request_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token?client_id={cliend_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}'.format(
            cliend_id=APP_ID,
            redirect_uri=URL_LOGIN_FACEBOOK,
            client_secret=SECRET_ID,
            code=code
        )
        r = requests.get(url_request_access_token)
        dict_access_token = r.json()
        print(json.dumps(dict_access_token, indent=2))
        access_token = dict_access_token.get('access_token')

        url_request_user_id = 'https://graph.facebook.com/debug_token?input_token={it}&access_token={at}'.format(
            it=access_token, at=APP_ACCESS_TOKEN
        )
        r = requests.get(url_request_user_id)
        dict_user_id = r.json()
        # print(dict_user_id)
        print(json.dumps(dict_user_id, indent=2))
        user_id = dict_user_id['data'].get('user_id')

        url_request_user_info = 'https://graph.facebook.com/{uid}?fields=id,name,first_name,last_name,age_range,link,gender,locale,picture,timezone,updated_time,verified,email&access_token={access_token}'.format(
            uid=user_id, access_token=access_token
        )
        r = requests.get(url_request_user_info)
        dict_user_info = r.json()
        # print(dict_user_info)
        print(json.dumps(dict_user_info, indent=2))

        user = authenticate(user_info=dict_user_info)
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

        # ret = 'AccessToken : {at}<br><br>Code : {code}<br><br>UserID : {user_id}'.format(
        #     at=access_token,
        #     code=code,
        #     user_id=user_id
        # )
        # return HttpResponse(ret)