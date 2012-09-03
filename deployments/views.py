from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from common import _slugit
from projects.models import Project
from deployments.models import CloudProvider, Deployment
from deployments.forms import AssociateDeploymentForm


TEMPLATE_PATH = 'deployments/'


def _createParams(req):
    p = {'breadcrumbs': [{reverse('deployments'): 'Deployments'}],
        'is_deployments': True, 'nav_projects': Project.objects.filter( \
        owner=req.user).exclude(production_url__exact='')}
    p.update(csrf(req))
    p['deployments'] = Deployment.objects.filter(owner=req.user)
    return p


@login_required
def home(req):
    p = _createParams(req)
    return render_to_response(TEMPLATE_PATH + 'home.html', p, 
        context_instance=RequestContext(req))


@login_required
def deployment(req, slug=''):
    if req.method == 'GET':
        p = _createParams(req)
        deployment = get_object_or_404(Deployment, slug=slug)
        p['form'] = AssociateDeploymentForm(instance=deployment)
        p['slug'] = deployment.slug
        return render_to_response(TEMPLATE_PATH + 'associate.html', p, 
            context_instance=RequestContext(req))
    elif req.method == 'POST':
        deployment = get_object_or_404(Deployment, slug=slug)
        # check user permissions
        if deployment.owner == req.user:
            form = AssociateDeploymentForm(req.POST)
            if form.is_valid():
                _save_associate_deployment(form, deployment)
                messages.add_message(req, messages.INFO, 
                    'Deployment "%s" successfully updated.' % deployment.name)
                return HttpResponseRedirect(reverse('deployments'))
            else:
                return render_to_response(TEMPLATE_PATH + 'associate.html',
                    p, context_instance=RequestContext(req))
                
        else:
            messages.add_message(req, messages.INFO, 
                'You must be the owner of a deployment to edit it.')
            return HttpResponseRedirect(reverse('deployments'))
        

@login_required
def associate_deployment(req):
    p = _createParams(req)
    if req.method == 'GET':
        p['form'] = AssociateDeploymentForm()
        return render_to_response(TEMPLATE_PATH + 'associate.html', p, 
            context_instance=RequestContext(req))
    elif req.method == 'POST':
        form = AssociateDeploymentForm(req.POST)
        if form.is_valid():
            d = Deployment()
            d.owner = req.user
            _save_associate_deployment(form, d)
            messages.add_message(req, messages.INFO, 
                '%s successfully associated with %s.' % (d.project,
                d.provider))
            return HttpResponseRedirect(reverse('deployments'))
        else:
            p['form'] = form
            return render_to_response(TEMPLATE_PATH + 'associate.html', p, 
                context_instance=RequestContext(req))


def _save_associate_deployment(form, d):
    d.name = form.cleaned_data['name']
    d.slug = _slugit(Deployment, d.name)
    d.provider = form.cleaned_data['provider']
    d.project = form.cleaned_data['project']
    d.username = form.cleaned_data['username']
    d.ip_address = form.cleaned_data['ip_address']
    d.ssh_port = form.cleaned_data['ssh_port']
    d.save()

