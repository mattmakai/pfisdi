from django.conf.urls.defaults import *

urlpatterns = patterns('core.views',
    url(r'^$', 'sign_in', name='sign_in'),
    url(r'^sign-out/$', 'sign_out', name='sign_out'),
)
