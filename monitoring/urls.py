from django.conf.urls.defaults import *

urlpatterns = patterns('monitoring.views',
    url(r'^$', 'home', name='monitoring'),
)
