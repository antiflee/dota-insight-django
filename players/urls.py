from django.conf.urls import url

from . import views

app_name = 'players'

urlpatterns = [
    url(r'^$', views.players, name='playersHome'),
    url(r'^realTimeRegion$', views.realTimeRegion, name='realTimeRegion'),
    url(r'^DAU$', views.DAU, name='DAU'),
    url(r'^(?P<account_id>\d+)/$', views.playerDetail, name='playerDetail'),
    url(r'^(?P<account_id>\d+)/getPlayerActivityHistory$', views.getPlayerActivityHistory, name='getPlayerActivityHistory'),
]
