from ..models import Post
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ..forms import PostForm


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(data=request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'projects/blog/post_edit.html', {'form': form})
