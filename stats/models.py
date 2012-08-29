from django.db import models
from projects.models import Project

class AppCounter(models.Model):
    app = models.ForeignKey(Project)
    created = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField() 
