from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager, PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_facebook_user(self, user_info):
        user = self.model(
            facebook_id=user_info.get('id'),
            email=user_info.get('email'),
            last_name=user_info.get('last_name', ''),
            first_name=user_info.get('first_name', ''),
        )
        user.is_facebook_user = True
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class MyUser(AbstractBaseUser):
    CHOICES_GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    email = models.EmailField(max_length=100, unique=True)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    joined_date = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=10, choices=CHOICES_GENDER, blank=True)
    is_staff = models.BooleanField(default=False)
    nickname = models.CharField(max_length=30, blank=True)
    img_profile = models.ImageField(upload_to='user', blank=True)
    img_profile_thumbnail = models.ImageField(upload_to='user/thumbnail', blank=True)

    # Facebook user
    is_facebook_user = models.BooleanField(default=False)
    facebook_id = models.CharField(max_length=50, blank=True)
    facebook_token = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return '%s%s' % (self.last_name, self.first_name)

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def short_name(self):
        return self.get_short_name()

    def make_thumbnail(self):
        from PIL import Image
        if self.img_profile:
            im = Image.open(self.img_profile.file.name)