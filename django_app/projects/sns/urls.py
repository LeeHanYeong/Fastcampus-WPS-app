from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^friends_ranking/$', views.friends_ranking, name='friends_ranking'),
    url(r'^friends_ranking_saved/$', views.friends_ranking_saved_list, name='friends_ranking_saved_list'),
    url(r'^friends_ranking_saved/(?P<pk>\d+)/$', views.friends_ranking_saved, name='friends_ranking_saved'),
]
