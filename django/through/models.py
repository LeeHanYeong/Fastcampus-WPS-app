from django.db import models

class Contact(models.Model):
    contacts = models.ManyToManyField('self', through='ContactRelationship', symmetrical=False)

class ContactRelationship(models.Model):
    note = models.CharField(max_length=100)
    from_contact = models.ForeignKey('Contact', related_name='from_contacts')
    to_contact = models.ForeignKey('Contact', related_name='to_contacts')

    class Meta:
        unique_together = ('from_contact', 'to_contact')

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)


class Topping(models.Model):
    title = models.CharField(max_length=50)


class Pizza(models.Model):
    title = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)


class 피자(models.Model):
    피자이름 = models.CharField(max_length=100)