from django.conf.urls import url

from . import views

app_name = 'heroes'

urlpatterns = [
    url(r'^$', views.heroes, name='heroesHome'),
    url(r'^winrate$', views.getHeroesWinRate, name='heroesWinRate'),
]
