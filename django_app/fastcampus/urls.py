from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from . import apis

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^projects/', include('projects.urls')),
    url(r'^member/', include('member.urls', namespace='member')),

    url(r'^markdownx/', include('markdownx.urls')),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^api/login/', include('rest_social_auth.urls_token')),

    url(r'^$', views.index, name='index'),
    url(r'^api/test/$', apis.TestApiView.as_view(), name='test_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
