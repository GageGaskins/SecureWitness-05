__author__ = 'Gage'

from django.conf.urls import patterns, url

from SecureWitness import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^reports/', views.reports, name='reports'),
    url(r'^report/(?P<report_id>[0-9]+)/$', views.report, name='report'),
    url(r'^report/(?P<report_id>[0-9]+)/edit_report_page/', views.edit_report_page, name='edit_report_page'),
    url(r'^report/(?P<report_id>[0-9]+)/update_report', views.update_report, name='update_report'),
    url(r'^report/(?P<report_id>[0-9]+)/delete_report', views.delete_report, name='delete_report'),
    url(r'^report/(?P<report_id>[0-9]+)/comment/', views.make_comment, name='make_comment'),
    url(r'^user/$', views.user, name='user'),
    url(r'^user/folder/(?P<folder_id>[0-9]+)/$', views.folder, name='folder'),
    url(r'^user/new_folder/', views.new_folder, name='new_folder'),
    url(r'^user/create_folder/', views.create_folder, name='create_folder'),
    url(r'^user/manage_folders', views.manage_folders, name='manage_folders'),
    url(r'^user/folder/(?P<folder_id>[0-9]+)/folder_add_report_list/', views.folder_add_report_list, name='folder_add_report_list'),
    url(r'^user/folder/(?P<folder_id>[0-9]+)/add_report/(?P<report_id>[0-9]+)/', views.folder_add_report, name='folder_add_report'),
    url(r'^user/folder/(?P<folder_id>[0-9]+)/folder_remove_report_list/', views.folder_remove_report_list, name='folder_remove_report_list'),
    url(r'^user/folder/(?P<folder_id>[0-9]+)/remove_report/(?P<report_id>[0-9]+)', views.folder_remove_report, name='folder_remove_report'),
    url(r'^user/folder/edit_folder_page/(?P<folder_id>[0-9]+)/', views.edit_folder_page, name='edit_folder_page'),
    url(r'^user/folder/update_folder/(?P<folder_id>[0-9]+)', views.update_folder, name='update_folder'),
    url(r'^user/folder/delete_folder(?P<folder_id>[0-9]+)/', views.delete_folder, name='delete_folder'),
    url(r'^user/new_report/$', views.new_report, name='new_report'),
    url(r'^user/create_report/$', views.create_report, name='create_report'),
    url(r'^group/(?P<group_id>[0-9]+)/$', views.group, name='group'),
    url(r'^group/(?P<group_id>[0-9]+)/share_report(?P<report_id>[0-9]+)/$', views.group_share_report, name='group_share_report'),
    url(r'^group/(?P<group_id>[0-9]+)/add_user(?P<user_id>[0-9]+)/$', views.group_add_user, name='group_add_user'),
    url(r'^search', views.search, name='search'),
    url(r'^list/$', views.doc_list, name='list'),
    url(r'^documents/(?P<docname>\w+)/', views.get_doc, name='get_doc'),
    url(r'^user/make_admin_list/$', views.make_admin_list, name='make_admin_list'),
    url(r'^user/make_admin/(?P<user_id>[0-9]+)/', views.make_admin, name='make_admin'),
    url(r'^user/manage_groups/', views.manage_groups, name='manage_groups'),
    url(r'^user/new_group/', views.new_group, name='new_group'),
    url(r'^user/create_group/', views.create_group, name='create_group'),
)

