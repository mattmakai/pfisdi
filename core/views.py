from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from common import _json_response
from core.models import Owner
from projects.models import Project
from taggit.models import Tag, TaggedItem
from ideas.models import Idea, ResearchLink
import re

TEMPLATE_PATH = 'core/'


@csrf_protect
def sign_in(req):
    if req.method == 'GET':
        if req.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard'))
        p = {}
        p.update(csrf(req))
        return render_to_response(TEMPLATE_PATH + 'signin.html', p, 
            context_instance=RequestContext(req))
    elif req.method == 'POST':
        username = req.POST.get('username', '')
        password = req.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is None:
            return _json_response('Invalid sign in.')
        elif user.is_active:
            login(req, user)
            return _json_response({'redirect': reverse('dashboard')})
        else:
            return _json_response("failure")


@login_required
def sign_out(req):
    logout(req)
    return HttpResponseRedirect('/')

