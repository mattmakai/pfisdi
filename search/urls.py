from django.conf.urls.defaults import *

urlpatterns = patterns('search.views',
    url(r'^$', 'tag_search', name='tag_search'),
    url(r'^all/(?P<term>[^/]+)/$', 'tag_search', name='tag_search'),
)
