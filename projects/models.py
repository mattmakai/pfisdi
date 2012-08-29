from django.db import models
from core.models import PFISDIModel
from taggit.managers import TaggableManager

class Project(PFISDIModel):
    repository_url = models.CharField(max_length=2048, blank=True, null=True)
    production_url = models.CharField(max_length=2048, blank=True, null=True)
    tags = TaggableManager()
