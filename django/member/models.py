from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager, PermissionsMixin
from fastcampus.models import BaseModel
from course.models import Course


class FastcampusUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(
            username=username,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, password):
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class FastcampusUser(AbstractBaseUser, PermissionsMixin):
    CHOICES_OBJECTIVE = (
        ('job', '취업'),
        ('change', '커리어 전환'),
        ('foundation', '창업'),
        ('interest', '흥미'),
    )
    """
    username
    first_name
    last_name
    email
    is_staff
    is_active
    date_joined
    """
    username = models.CharField('아이디', max_length=16, unique=True)
    last_name = models.CharField('성', max_length=30)
    first_name = models.CharField('이름', max_length=30)
    email = models.EmailField('이메일')
    course = models.ForeignKey(Course, verbose_name='수강 코스', null=True)
    github = models.CharField('GitHub계정 이름', max_length=50)
    age = models.IntegerField('나이', default=0)
    objective_type = models.CharField('목표', max_length=20, choices=CHOICES_OBJECTIVE)
    objective_detail = models.TextField('상세 목표', blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = [username]
    USERNAME_FIELD = 'username'

    objects = FastcampusUserManager()

    def __str__(self):
        return '%s (%s)' % (self.get_full_name(), self.course.full_title)

    def get_full_name(self):
        return '%s%s' % (self.last_name, self.first_name)

    def get_short_name(self):
        return '%s%s' % (self.last_name, self.first_name)