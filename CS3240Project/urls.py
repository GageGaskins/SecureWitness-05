from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CS3240Project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^SecureWitness/', include('SecureWitness.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
