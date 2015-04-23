__author__ = 'Gage'

from django.conf.urls import patterns, url

from SecureWitness import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^report/(?P<report_id>[0-9]+)/$', views.report, name='report'),
    url(r'^report/(?P<report_id>[0-9]+)/edit_report_page/', views.edit_report_page, name='edit_report_page'),
    url(r'^report/(?P<report_id>[0-9]+)/update_report', views.update_report, name='update_report'),
    url(r'^user/$', views.user, name='user'),
    url(r'^user/new_report/$', views.new_report, name='new_report'),
    url(r'^user/create_report/$', views.create_report, name='create_report'),
    url(r'^search', views.search, name='search'),
    url(r'^list/$', views.list, name='list'),
    url(r'^documents/(?P<docname>\w+)/', views.get_doc, name='get_doc'),
    url(r'^user/make_admin_list/$', views.make_admin_list, name='make_admin_list'),
    url(r'^user/make_admin/(?P<user_id>[0-9]+)/', views.make_admin, name='make_admin'),
)

