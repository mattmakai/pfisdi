from django.conf.urls.defaults import *

urlpatterns = patterns('marketing.views',
  url(r'^$', 'home', name='marketing'),
)
