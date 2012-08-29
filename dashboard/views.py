from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

from projects.models import Project


TEMPLATE_PATH = 'dashboard/'

def _create_params(req):
    p = {'breadcrumbs': [{reverse('dashboard'): 'Dashboard'}], 
        'is_dashboard': True, 'nav_projects': Project.objects.filter( \
        owner=req.user).exclude(production_url='')}
    p.update(csrf(req))
    return p


@login_required
def dashboard(req):
    p = _create_params(req)
    p['projects'] = Project.objects.filter(owner=req.user)
    return render_to_response(TEMPLATE_PATH + 'dashboard.html', p,
        context_instance=RequestContext(req))

