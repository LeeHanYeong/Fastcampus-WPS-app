import os
from PIL import Image, ImageOps
from io import StringIO, BytesIO
from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from fastcampus.models import BaseModel


class Album(BaseModel):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    img_cover = models.ImageField(upload_to='album', blank=True)
    like_count = models.IntegerField(default=0)
    photo_like_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Photo(BaseModel):
    album = models.ForeignKey(Album)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=60, blank=True)
    img = models.ImageField(upload_to='photo')
    img_thumbnail = models.ImageField(upload_to='photo/thumbnail', blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PhotoLike', related_name='photo_set_like_users')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PhotoDislike', related_name='photo_set_dislike_users')
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)

    def __str__(self):
        return '%s - %s' % (self.album.title, self.title)

    def save(self, *args, **kwargs):
        image_changed = False
        if self.img and not self.img_thumbnail:
            image_changed = True

        elif self.pk is not None:
            ori = Photo.objects.get(pk=self.pk)
            if ori.img != self.img:
                image_changed = True
        super().save(*args, **kwargs)

        if image_changed:
            self.make_thumbnail()
            super().save(*args, **kwargs)

    def url_img(self):
        return self.url_field('img')

    def url_thumbnail(self):
        return self.url_field('img_thumbnail')

    def detail(self, user=None):
        return {
            'photo': self,
            'user_like': self.user_like(user, like_type='like'),
            'user_dislike': self.user_like(user, like_type='dislike'),
            'like_count': self.like_users.count(),
            'dislike_count': self.dislike_users.count(),
        }

    def user_like(self, user, like_type='like'):
        if user is None or not user.is_authenticated():
            return False
        if like_type == 'like':
            if user in self.like_users.all():
                return True
        else:
            if user in self.dislike_users.all():
                return True
        return False

    def make_thumbnail(self):
        size = (300, 300)
        f = default_storage.open(self.img)
        image = Image.open(f)

        ftype = image.format
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        path, ext = os.path.splitext(self.img.name)
        name = os.path.basename(path)
        thumbnail_name = '%s_thumb%s' % (name, ext)
        temp_file = BytesIO()
        image.save(temp_file, ftype)
        temp_file.seek(0)

        self.img_thumbnail.save(thumbnail_name, ContentFile(temp_file.read()))
        temp_file.close()
        f.close()
        return True


class PhotoLike(BaseModel):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class PhotoDislike(BaseModel):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)