from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from ..models import Post


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        return redirect('blog:post_list')
    else:
        messages.error(request, '삭제 권한이 없습니다')
        raise PermissionDenied
