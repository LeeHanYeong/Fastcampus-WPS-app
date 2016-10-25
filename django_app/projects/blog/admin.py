from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'admin_img_cover', )
    search_fields = ('title', 'text', )

admin.site.register(Post, PostAdmin)