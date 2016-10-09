from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager, PermissionsMixin
from fastcampus.models import BaseModel
from course.models import Course


class User(AbstractUser, PermissionsMixin):
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
    course = models.ForeignKey(Course, verbose_name='수강 코스')
    github = models.CharField('GitHub계정 이름', max_length=50)
    age = models.IntegerField('나이', default=0)
    objective_type = models.CharField('목표', max_length=20, choices=CHOICES_OBJECTIVE)
    objective_detail = models.TextField('상세 목표', blank=True)

    def __str__(self):
        return '%s (%s)' % (self.get_full_name(), self.course.full_title)

    def get_full_name(self):
        return '%s%s' % (self.last_name, self.first_name)