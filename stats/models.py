from django.db import models
from deployments.models import Deployment

class AppCounter(models.Model):
    deployment = models.ForeignKey(Deployment)
    created = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField() 

class CPUUtilization(models.Model):
    deployment = models.ForeignKey(Deployment)
    created = models.DateTimeField(auto_now_add=True)
    utilization = models.DecimalField(max_digits=7, decimal_places=2)
    interval = models.IntegerField("interval in seconds")
    def __unicode__(self):
        return u"%s:%s" % (str(self.deployment), str(self.utilization))
