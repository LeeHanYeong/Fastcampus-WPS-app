from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)


class Answer(models.Model):

    content = models.TextField()