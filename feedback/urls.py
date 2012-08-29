from django.conf.urls.defaults import *

urlpatterns = patterns('feedback.views',
    url(r'^$', 'home', name='feedback'),
)
