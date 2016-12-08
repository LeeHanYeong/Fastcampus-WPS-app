from django.contrib import admin
from django.db import models
from markdownx.widgets import AdminMarkdownxWidget
from adminsortable.admin import SortableAdmin

from fastcampus.utils.admin import SortableAdmin
from .models import *


class LectureAdmin(SortableAdmin):
    formfield_overrides = {
        models.TextField: {
            'widget': AdminMarkdownxWidget,
        }
    }


admin.site.register(Course)
admin.site.register(LectureSection)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(LectureVideo)