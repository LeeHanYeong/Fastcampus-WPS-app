import requests
import json
from collections import Counter
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

__all__ = [
    'friends_ranking',
]


def friends_ranking(request):
    APP_ID = '338774269808826'
    SECRET_ID = 'b780a89551228b4c1015c529a7667722'
    APP_ACCESS_TOKEN = '%s|%s' % (APP_ID, SECRET_ID)
    URL_REDIRECT = '{}{}'.format('http://localhost:8081', reverse('sns:friends_ranking'))

    print('URL_REDIRECT : %s' % URL_REDIRECT)
    if request.GET.get('error'):
        messages.error(request, '사용자에 의해 페이스북 로그인 거부')
        return redirect('member:login')

    if request.GET.get('code'):
        code = request.GET.get('code')
        print('code: %s' % code)
        url_request_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token?' \
                                   'client_id={cliend_id}&' \
                                   'redirect_uri={redirect_uri}&' \
                                   'client_secret={client_secret}&' \
                                   'code={code}'.format(
            cliend_id=APP_ID,
            redirect_uri=URL_REDIRECT,
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
        # print(json.dumps(dict_user_id, indent=2))
        user_id = dict_user_id['data'].get('user_id')

        url_request_feed = 'https://graph.facebook.com/{uid}/feed?' \
                           'limit=10000&' \
                           'since=2013-01-01&' \
                           'until=2016-12-31&' \
                           'fields=comments&' \
                           'access_token={access_token}'.format(
            uid=user_id, access_token=access_token
        )
        r = requests.get(url_request_feed)
        dict_feed_info = r.json()
        # print(dict_user_info)
        # print(json.dumps(dict_feed_info))

        comment_list = []
        for feed in dict_feed_info.get('data'):
            if feed.get('comments'):
                for comment in feed.get('comments').get('data'):
                    comment_list.append(comment)

        counter = Counter()
        id_list = [comment.get('from', {}).get('id') for comment in comment_list]
        for id in id_list:
            counter[id] += 1

        most_list = counter.most_common()
        most_id_list = [item[0] for item in most_list]
        str_most_id_list = ','.join(most_id_list)
        print(most_id_list)

        url_request_friends = 'https://graph.facebook.com/?ids={ids}&' \
                              'fields=cover,email,picture.width(500).height(500),name&' \
                              'access_token={access_token}'.format(
            ids=str_most_id_list,
            access_token=access_token
        )
        r = requests.get(url_request_friends)
        dict_friends_info = r.json()

        most_dict_list = []
        for most in most_list:
            id = most[0]
            for k in dict_friends_info:
                if k == id and k != user_id:
                    most_dict_list.append({
                        'info': dict_friends_info[k],
                        'number': most[1],
                    })

        # for item in most_dict_list:
        #     info = item[0]
        #     number = item[1]
        #     print('%s : %s' % (info['name'], number))
        context = {
            'most_dict_list': most_dict_list
        }
        return render(request, 'projects/sns/facebook/friends_ranking.html', context)