from django.conf.urls.defaults import *

urlpatterns = patterns('stats.views',
  url(r'^homepage-counter/$', 'homepage_counter'),
  url(r'^cpu-utilization/$', 'cpu_utilization'),
)
