from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from ..forms import PostForm


def post_new(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse('로그인하세요!')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # 앞의 blog는 mysite/urls.py의 include('blog.urls')의 namespace
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'projects/blog/post_new.html', {'form': form})