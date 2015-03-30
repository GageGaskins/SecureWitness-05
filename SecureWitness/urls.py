__author__ = 'Gage'

from django.conf.urls import patterns, url

from SecureWitness import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'user', views.user, name='user'),
)

