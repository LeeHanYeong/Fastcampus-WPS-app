from django.db import models
from django.conf import settings
from fastcampus.models import BaseModel

__all__ = [
    'FriendsRanking',
    'FriendsRankingItem',
]


class FriendsRanking(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class FriendsRankingItem(BaseModel):
    parent = models.ForeignKey(FriendsRanking)
    facebook_user_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    url_profile = models.URLField(blank=True)
    comment_count = models.IntegerField(default=0)
