from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from ..forms import VideoModelForm
from ..models import Video
from ..apis.youtube import youtube_search_detail, youtube_search_list
__all__ = [
    'search',
    'search_detail',
]


def items_add_extra_info(items):
    for item in items:
        form = VideoModelForm(
            initial={
                'kind': item.get('kind'),
                'youtube_id': item.get('id'),
                'title': item.get('snippet').get('title'),
                'description': item.get('snippet').get('description'),
                'published_date': parse_datetime(item.get('snippet').get('publishedAt')),
                'thumbnail_url': item.get('snippet').get('thumbnails').get('high').get('url'),
            }
        )
        item['form'] = form
        if Video.objects.filter(youtube_id=item.get('id')).exists():
            item['is_exist'] = True
    return items


def search(request):
    context = {}
    keyword = request.GET.get('keyword')
    response = youtube_search_list(keyword)

    response['items'] = items_add_extra_info(response['items'])

    if keyword:
        context = {
            'keyword': keyword,
            'response': response,
        }
    return render(request, 'projects/video/search.html', context)


def search_detail(request, video_id):
    response = youtube_search_detail(video_id)
    response['items'] = items_add_extra_info(response['items'])
    context = {
        'response': response,
    }
    return render(request, 'projects/video/search_detail.html', context)
