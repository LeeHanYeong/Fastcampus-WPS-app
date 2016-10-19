from django.db import models


class Group(models.Model):
    pass


class Person(models.Model):
    group = models.ForeignKey(Group)


class MyPerson(Person):
    class Meta:
        proxy = True


class Animal(models.Model):
    group = models.ForeignKey(Group, related_name='group_set')
    other_group = models.ForeignKey(Group, related_name='other_group_set')


class Base(models.Model):
    group = models.ForeignKey(Group, related_name="%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True


class ChildA(Base):
    pass


class ChildB(Base):
    pass