from django.db import models
from fastcampus.models import BaseModel
# from member.models import FastcampusUser as User



class Quiz(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Answer(BaseModel):
    # user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    content = models.TextField()

    def __str__(self):
        return '%s 답변(%s)' % (self.quiz.title, self.user.get_full_name())