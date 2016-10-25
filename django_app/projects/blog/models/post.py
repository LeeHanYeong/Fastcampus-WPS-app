from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.safestring import mark_safe

__all__ = ['Post']


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=50)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)
    img_cover = models.ImageField(upload_to='post', blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def admin_img_cover(self):
        return mark_safe('<img src="/media/%s" height="150px"' % self.img_cover)
    admin_img_cover.short_description = '커버 이미지'
