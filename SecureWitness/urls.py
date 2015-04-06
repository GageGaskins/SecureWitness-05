__author__ = 'Gage'

from django.conf.urls import patterns, url

from SecureWitness import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^report/(?P<report_id>[0-9]+)', views.report, name='report'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
)

