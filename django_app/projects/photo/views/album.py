from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import messages
from ..models import Album, Photo, PhotoLike
from ..forms.album import AlbumForm

__all__ = [
    'album_list',
    'album_detail',
    'album_add',
]


def album_list(request):
    albums = Album.objects.all()
    context = {
        'albums': albums,
    }
    return render(request, 'projects/photo/album_list.html', context)


def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    context = {
        'album': album,
    }
    # template_file = 'projects/photo/album_detail.html'
    template_file = 'projects/photo/ajax_album_detail.html'
    return render(request, template_file, context)


@login_required
def album_add(request):
    if request.method == 'GET':
        form = AlbumForm()
    else:
        form = AlbumForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']

            album = Album.objects.create(
                title=title,
                description=description,
                owner=request.user
            )
            return redirect('photo:album_detail', pk=album.pk)
    context = {
        'form': form,
    }
    return render(request, 'projects/photo/album_add.html', context)