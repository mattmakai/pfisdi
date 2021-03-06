from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.conf import settings

from deployments.models import Deployment
from stats.models import AppCounter, CPUUtilization
from common import _json_response


@csrf_exempt
def homepage_counter(req):
    if req.method == 'POST':
        if req.POST.get('handshake').strip() == settings.STATS_SECRET_KEY:
            proj = get_object_or_404(Project, 
                name=req.POST.get('deployment_key'))
            ac = AppCounter()
            try:
                ac = AppCounter.objects.get(app=proj)
                ac.counter = ac.counter + 1
            except ObjectDoesNotExist as dne:
                ac.app = proj
                ac.counter = 1
            ac.save()
        return _json_response('ok')


@csrf_exempt
def cpu_utilization(req):
    try:
        print req
        if req.method == 'POST':
            #if req.POST.get('handshake').strip() == settings.STATS_SECRET_KEY:
            deployment = get_object_or_404(Deployment, id=1)
            #            name=req.POST.get('deployment_key'))
            for utilization in req.POST.getlist('utilizations'):
                u = CPUUtilization()
                u.deployment = deployment
                u.interval = req.POST.get('interval')
                u.utilization = utilization
                u.save()
            print req.POST
            return HttpResponse('ok')
    except Exception as e:
        print e

