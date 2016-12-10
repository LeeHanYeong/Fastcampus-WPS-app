from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from . import apis

apis_patterns = [
    url(r'^course/', include('course.urls.apis')),
]
view_patterns = [

]

urlpatterns = [
    # include 3rd-party applications
    url(r'^admin/', admin.site.urls),
    url(r'^markdownx/', include('markdownx.urls')),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),

    # include created applications
    url(r'^projects/', include('projects.urls')),
    url(r'^member/', include('member.urls', namespace='member')),

    # views
    url(r'^$', views.index, name='index'),

    # apis
    url(r'^api/', include(apis_patterns)),
    # url(r'^api/login/', include('rest_social_auth.urls_token')),
    # url(r'^api/test/$', apis.TestApiView.as_view(), name='test_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
