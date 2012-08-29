from django.conf.urls.defaults import *

urlpatterns = patterns('deployments.views',
    url(r'^$', 'home', name='deployments'),
    url(r'^associate/$', 'associate_deployment', name='associate_deployment'),
    url(r'^(?P<slug>[a-zA-Z0-9\-]+)/$', 'deployment', name='deployment'),
)
