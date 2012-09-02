from django.db import models
from django.contrib.auth.models import User
from core.models import PFISDIModel
from projects.models import Project
from taggit.managers import TaggableManager

class CloudProvider(PFISDIModel):
    pass


class Deployment(PFISDIModel):
    project = models.ForeignKey(Project)
    provider = models.ForeignKey(CloudProvider)
    username = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.CharField(max_length=32, blank=True, null=True)
    ssh_port = models.IntegerField(blank=True, null=True)
    is_production = models.BooleanField(default=False)
    # deployment_key = models.CharField(max_length=255, unique=True)
    def ssh_command(self):
        return 'ssh -p %s %s@%s' % (str(ssh_port), username, ip_address)

