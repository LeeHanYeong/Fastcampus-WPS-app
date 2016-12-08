from django.contrib import admin
from adminsortable.admin import SortableAdmin as OriSortableAdmin


class BaseAdmin(admin.ModelAdmin):
    class Meta:
        abstract = True


class SortableAdmin(OriSortableAdmin, BaseAdmin):
    pass