from django.db import models


class Channel(models.Model):
    youtube_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Video(models.Model):
    channel = models.ForeignKey(Channel, null=True, blank=True)
    kind = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    published_date = models.DateTimeField()
    created_date = models.DateField(auto_now_add=True)
    thumbnail_url = models.URLField()
    thumbnail_img = models.ImageField(upload_to='video', blank=True)

    def __str__(self):
        return self.title