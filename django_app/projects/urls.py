from django.conf.urls import url, include
from . import views

urlpatterns = [
    # url(r'^$', views.index, name='')
    url(r'^member/', include('member.urls', namespace='member')),
    url(r'^blog/', include('projects.blog.urls', namespace='blog')),
    url(r'^video/', include('projects.video.urls', namespace='video')),
    url(r'^sns/', include('projects.sns.urls', namespace='sns')),
]
