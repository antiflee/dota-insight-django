from django.conf.urls import url

from . import views

app_name = 'utils'

urlpatterns = [
    url(r'^slides$', views.slides, name='googleSlides'),
    url(r'^code$', views.sourceCode, name='sourceCode'),
]
