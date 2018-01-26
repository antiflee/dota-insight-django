from django.conf.urls import url

from . import views

app_name = 'players'

urlpatterns = [
    url(r'^$', views.players, name='playersHome'),
    url(r'^realTimeRegion$', views.realTimeRegion, name='realTimeRegion'),
]
