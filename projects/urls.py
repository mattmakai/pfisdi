from django.conf.urls.defaults import *

urlpatterns = patterns('projects.views',
    url(r'^$', 'home', name='projects'),
    url(r'new/project/$', 'new_project', name='new_project'),
    url(r'project/(?P<slug>[a-zA-Z0-9\-]+)/$', 'project', name='project'),
)
