from django.contrib import admin
from .models import Album, Photo


class PhotoInline(admin.TabularInline):
    model = Photo


class AlbumAdmin(admin.ModelAdmin):
    inlines = (PhotoInline, )


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo)