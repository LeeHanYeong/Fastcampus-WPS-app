from django.conf.urls import url, include

urlpatterns = [
    url(r'^member/', include('member.urls', namespace='member')),
    url(r'^blog/', include('projects.blog.urls', namespace='blog')),
    url(r'^video/', include('projects.video.urls', namespace='video')),
    url(r'^sns/', include('projects.sns.urls', namespace='sns')),
]
