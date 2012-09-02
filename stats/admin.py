from django.contrib import admin
from models import AppCounter, CPUUtilization

admin.site.register(AppCounter)
admin.site.register(CPUUtilization)
