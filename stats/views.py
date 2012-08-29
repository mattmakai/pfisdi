from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.conf import settings

from projects.models import Project
from models import AppCounter
from common import _json_response


@csrf_exempt
def homepageCounter(req):
    if req.method == 'POST':
        if req.POST.get('handshake').strip()  == settings.STATS_SECRET_KEY:
            proj = get_object_or_404(Project, name=req.POST.get('app_name'))
            ac = AppCounter()
            try:
                ac = AppCounter.objects.get(app=proj)
                ac.counter = ac.counter + 1
            except ObjectDoesNotExist as dne:
                ac.app = proj
                ac.counter = 1
            ac.save()
        return _json_response('ok')

