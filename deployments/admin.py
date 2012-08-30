from django.contrib import admin
from deployments.models import CloudProvider, Deployment

admin.site.register(CloudProvider)
admin.site.register(Deployment)
