from django.contrib import messages
from django.shortcuts import render, redirect
from ..models import Video
from ..forms import VideoModelForm
__all__ = [
    'bookmark_list',
    'bookmark_add',
    'bookmark_detail',
]


def bookmark_list(request):
    videos = Video.objects.all()
    context = {
        'videos': videos
    }
    return render(request, 'video/bookmark_list.html', context)


def bookmark_add(request):
    form = VideoModelForm(request.POST)
    path = request.POST.get('path')
    if form.is_valid():
        instance = form.save()
        messages.success(request, '\'{}\' 영상이 북마크 되었습니다'.format(instance.title))

    else:
        messages.error(request, '북마크 추가 중 에러가 발생하였습니다')
        # return HttpResponse(form.as_table())

    if path:
        return redirect(path)
    return redirect('video:search')


def bookmark_detail(request, pk):
    video = Video.objects.get(pk=pk)
    context = {
        'video': video,
    }
    return render(request, 'video/bookmark_detail.html', context)