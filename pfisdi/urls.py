from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('core.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^ideas/', include('ideas.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^deployments/', include('deployments.urls')),
    url(r'^monitoring/', include('monitoring.urls')),
    url(r'^marketing/', include('marketing.urls')),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^iterate/', include('iterate.urls')),
    url(r'^finance/', include('finance.urls')),
    url(r'^stats/', include('stats.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
