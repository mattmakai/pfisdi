from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from projects.models import Project
from common import _json_response

TEMPLATE_PATH = 'feedback/'

def _create_params(req):
    p = {'breadcrumbs': [{reverse('feedback'): 'Feedback'}], 
        'is_feedback': True, 'nav_projects': Project.objects.filter( \
        owner=req.user).exclude(production_url__exact='')}
    p.update(csrf(req))
    return p


@login_required
def home(req):
    p = _create_params(req)
    return render_to_response(TEMPLATE_PATH + 'home.html', p,
        context_instance=RequestContext(req))

