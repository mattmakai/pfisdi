from django.conf.urls.defaults import *

urlpatterns = patterns('finance.views',
  url(r'^$', 'home', name='finance'),
)
