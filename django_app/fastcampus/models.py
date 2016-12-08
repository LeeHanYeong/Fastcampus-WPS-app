from django.db import models
from adminsortable.models import SortableMixin


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(BaseModel, self).save(*args, **kwargs)

    def url_field(self, fieldname):
        field = getattr(self, fieldname)
        if field and hasattr(field, 'url'):
            return field.url


class PriorityMixin(SortableMixin):
    priority = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ('priority', )
