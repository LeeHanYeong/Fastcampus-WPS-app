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
from apis import facebook
from member.forms import LoginForm
from ..models import FriendsRanking, FriendsRankingItem
User = get_user_model()

__all__ = [
    'friends_ranking',
    'friends_ranking_saved',
    'friends_ranking_saved_list',
]


def friends_ranking(request):
    if request.method == 'GET':
        redirect_uri = '{}{}'.format('http://%s' % request.META['HTTP_HOST'], reverse('sns:friends_ranking'))

        if request.GET.get('error'):
            messages.error(request, '사용자에 의해 페이스북 로그인 거부')
            return redirect('member:login')

        if request.GET.get('code'):
            code = request.GET.get('code')

            access_token = facebook.get_access_token(code, redirect_uri)
            user_id = facebook.get_user_id_from_access_token(access_token)
            url_request_feed = 'https://graph.facebook.com/v2.8/{user_id}/feed?' \
                               'limit=10000&' \
                               'since=2013-01-01&' \
                               'until=2016-12-31&' \
                               'fields=comments&' \
                               'access_token={access_token}'.format(
                                    user_id=user_id,
                                    access_token=access_token
                                )
            r = requests.get(url_request_feed)
            dict_feed_info = r.json()

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

            url_request_friends = 'https://graph.facebook.com/v2.8/?ids={ids}&' \
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

            context = {
                'facebook_user_id': user_id,
                'access_token': access_token,
                'most_dict_list': most_dict_list
            }
            return render(request, 'projects/sns/facebook/friends_ranking.html', context)

    elif request.method == 'POST':
        import ast
        user = request.user
        if not user.is_authenticated():
            access_token = request.POST['access_token']
            facebook_user_id = request.POST['facebook_user_id']
            user_info = facebook.get_user_info(facebook_user_id, access_token)
            user = authenticate(user_info=user_info)

        fr = FriendsRanking.objects.create(user=user)
        str_item_list = request.POST.getlist('item')
        for str_item in str_item_list:
            item = ast.literal_eval(str_item)
            facebook_user_id = item['info']['id']
            name = item['info']['name']
            url_profile = item['info']['picture']['data']['url']
            comment_count = item['number']
            FriendsRankingItem.objects.create(
                parent=fr,
                facebook_user_id=facebook_user_id,
                name=name,
                url_profile=url_profile,
                comment_count=comment_count
            )
        return redirect('sns:friends_ranking_saved', pk=fr.pk)


def friends_ranking_saved_list(request):
    fr_list = FriendsRanking.objects.filter(user=request.user)
    context = {
        'fr_list': fr_list,
    }
    return render(request, 'projects/sns/facebook/friends_ranking_saved_list.html', context)


def friends_ranking_saved(request, pk=None):
    fr = FriendsRanking.objects.get(pk=pk)
    fri_list = FriendsRankingItem.objects.filter(parent=fr).order_by('-comment_count')
    context = {
        'fr': fr,
        'fri_list': fri_list,
    }
    return render(request, 'projects/sns/facebook/friends_ranking_saved.html', context)