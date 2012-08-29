from django.conf.urls.defaults import *

urlpatterns = patterns('ideas.views',
    url(r'^$', 'home', name='ideas'),
    url(r'^idea/new/$', 'new_idea', name='new_idea'),
    url(r'^idea/(?P<slug>[a-zA-Z0-9\-]+)/$', 'idea', name='idea'),
    url(r'^connections/$', 'connections', name='idea_connections'),
    url(r'^connections/add-idea/$', 'add_idea_to_connection', 
        name='add_idea_to_connections'),
    url(r'^new/research-link/$', 'new_research_link', 
        name='new_research_link'),
    url(r'^research-link/(?P<slug>[a-zA-Z0-9\-]+)/$', 'research_link',
        name='research_link'),
)
