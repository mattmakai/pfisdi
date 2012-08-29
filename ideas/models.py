from django.db import models
from django.contrib.auth.models import User
from core.models import PFISDIModel
from projects.models import Project
from taggit.managers import TaggableManager


class Idea(PFISDIModel):
    concept = models.TextField(blank=True)
    tags = TaggableManager()
    projects = models.ManyToManyField(Project)


class ResearchLink(PFISDIModel):
    link_url = models.CharField('Link URL', max_length=2048)
    tags = TaggableManager()
