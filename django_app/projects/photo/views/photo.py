from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import messages
from ..models import Album, Photo, PhotoLike, PhotoDislike
from ..forms.photo import PhotoForm

__all__ = [
    'photo_add',
    'photo_detail',
    'photo_like',
]


@login_required
def photo_add(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    if request.method == 'GET':
        form = PhotoForm()
    else:
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']

            photo = Photo(
                album=album,
                title=title,
                description=description,
                owner=request.user,
                img=request.FILES['img'],
            )
            photo.save()
            return redirect('photo:album_detail', pk=album.pk)
    context = {
        'form': form,
    }
    return render(request, 'projects/photo/photo_add.html', context)


def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    context = {
        'photo': photo,
    }
    return render(request, 'projects/photo/photo_detail.html', context)


@login_required
@require_POST
def photo_like(request, pk, like_type):
    next_path = request.GET.get('next', reverse('photo:photo_detail', kwargs={'pk':pk}))
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
    else:
        like_model.objects.create(
            user=request.user,
            photo=photo
        )
        opposite_model.objects.filter(user=request.user, photo=photo).delete()
    return redirect(next_path)