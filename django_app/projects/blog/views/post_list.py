from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from ..models import Post


def post_list(request):
    posts = Post.objects \
        .filter(
            Q(published_date__lte=timezone.now()) |
            Q(published_date=None)
        ).order_by('published_date')
    paginator = Paginator(posts, 3)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'post_list': posts,
        'title': '타이틀 변수는 title키를 이용해서 접근'
    }

    return render(request, 'projects/blog/post_list.html', context)
