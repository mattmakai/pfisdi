from django.db import models
from deployments.models import Deployment

class AppCounter(models.Model):
    deployment = models.ForeignKey(Deployment)
    created = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField() 

class CPUUtilization(models.Model):
    deployment = models.ForeignKey(Deployment)
    created = models.DateTimeField(auto_now_add=True)
    utilization = models.IntegerField()
    interval = models.IntegerField("interval in seconds")
