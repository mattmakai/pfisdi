from django.conf.urls.defaults import *

urlpatterns = patterns('stats.views',
  url(r'^homepage-counter/$', 'homepageCounter'),
)
