from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'admin_img_cover', )
    search_fields = ('title', 'text', )

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)