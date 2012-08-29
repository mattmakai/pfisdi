from django.db import models
from django.contrib.auth.models import User

class Owner(models.Model):
    user = models.ForeignKey(User)


class PFISDIModel(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)
    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        abstract = True

