from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^login/$', views.login1, name='login'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^login2/$', views.login2, name='login2'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/facebook/', views.login_facebook, name='login_facebook'),

    # url(r'^django-login/$', 'django.contrib.auth.views.login', name='django-login', kwargs={'template_name': 'login_django.html'})
]