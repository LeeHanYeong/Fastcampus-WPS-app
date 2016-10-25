from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'projects.blog'

    def ready(self):
        from . import signals