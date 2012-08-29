from django.conf.urls.defaults import *

urlpatterns = patterns('dashboard.views',
    url(r'^$', 'dashboard', name='dashboard'),
)
