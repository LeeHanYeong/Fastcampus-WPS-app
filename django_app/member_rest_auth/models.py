from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class MyUserManager(UserManager):
    pass


class MyUser(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True)
    img_profile = models.ImageField(upload_to='user', blank=True)
