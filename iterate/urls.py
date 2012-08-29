from django.conf.urls.defaults import *

urlpatterns = patterns('iterate.views',
  url(r'^$', 'home', name='iterate'),
)
