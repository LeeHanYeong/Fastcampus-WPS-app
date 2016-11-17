import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from ..models import Album, Photo, PhotoLike, PhotoDislike


__all__ = [
    'photo_like',
]


# @csrf_exempt
@require_POST
def photo_like(request, pk, like_type):
    photo = get_object_or_404(Photo, pk=pk)
    if like_type == 'like':
        like_model = PhotoLike
        opposite_model = PhotoDislike
    else:
        like_model = PhotoDislike
        opposite_model = PhotoLike

    like_exist = like_model.objects.filter(user=request.user, photo=photo)
    if like_exist.exists():
        like_exist.delete()
        msg = 'deleted'
    else:
        like_model.objects.create(
            user=request.user,
            photo=photo
        )
        opposite_model.objects.filter(user=request.user, photo=photo).delete()
        msg = 'created'
    ret = {
        'like_count': photo.like_users.count(),
        'dislike_count': photo.dislike_users.count(),
        'user_like': True if photo.like_users.filter(id=request.user.id).exists() else False,
        'user_dislike': True if photo.dislike_users.filter(id=request.user.id).exists() else False,
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')