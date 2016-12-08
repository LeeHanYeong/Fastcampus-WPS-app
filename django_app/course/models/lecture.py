from django.db import models
from markdownx.models import MarkdownxField
from fastcampus.models import BaseModel, PriorityMixin

__all__ = [
    'LectureSection',
    'Lecture',
    'LectureVideo',
]


class LectureSection(PriorityMixin, BaseModel):
    course = models.ForeignKey('course.Course', verbose_name='해당 코스')
    title = models.CharField('강의 섹션', max_length=100)
    description = models.TextField('섹션 설명', blank=True)

    def __str__(self):
        return self.title


class Lecture(PriorityMixin, BaseModel):
    section = models.ForeignKey('course.LectureSection', verbose_name='해당 섹션')
    title = models.CharField('강의 제목', max_length=100)
    description = models.TextField('강의 설명', blank=True)
    content = MarkdownxField('강의 내용', blank=True)

    def __str__(self):
        return self.title


class LectureVideo(BaseModel):
    lecture = models.ForeignKey('course.Lecture', verbose_name='해당 강의')
    title = models.CharField('영상 제목', max_length=100)
    description = models.CharField('영상 설명', max_length=200, blank=True)
    youtube_url = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.title
