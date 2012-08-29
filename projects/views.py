from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from ideas.models import Idea
from projects.models import Project
from projects.forms import ProjectForm
from common import _slugit, _json_response, _add_tags 

TEMPLATE_PATH = 'projects/'

def _createParams(req):
    p = {'breadcrumbs': [{reverse('projects'): 'Projects'}], 
        'is_projects': True, 'nav_projects': Project.objects.filter( \
        owner=req.user).exclude(production_url='')}
    p.update(csrf(req))
    return p
 

@login_required
def home(req):
    p = _createParams(req)
    p['projects'] = Project.objects.filter(owner=req.user).order_by('name')
    return render_to_response(TEMPLATE_PATH + 'home.html', p,
        context_instance=RequestContext(req))


@login_required
def new_project(req):
    p = _createParams(req)
    if req.method == 'GET':
        p['breadcrumbs'].append({reverse('new_project'): 'New Project'})
        p['ideas'] = Idea.objects.filter(owner=req.user)
        p['form'] = ProjectForm()
        return render_to_response(TEMPLATE_PATH + 'project.html', p,
            context_instance=RequestContext(req))
    elif req.method == 'POST':
        form = ProjectForm(req.POST)
        if form.is_valid():
            project = Project()
            project.owner = req.user
            _save_project(form, project)
            ideas = req.POST.get('ideas', '')
            tags = req.POST.get('tags', '').strip()
            if tags != '':
                _add_tags(project, tags, req.user, 'project')
            messages.add_message(req, messages.INFO, 
                'Project "%s" added successfully.' % project.name)
            return HttpResponseRedirect(reverse('projects'))
        else:
            p['form'] = form
            return render_to_response(TEMPLATE_PATH + 'project.html', p,
                context_instance=RequestContext(req))


@login_required
def project(req, slug=''):
    project = get_object_or_404(Project, slug=slug, owner=req.user)
    if req.method == 'GET':
        if req.user == project.owner:
            p = _createParams(req)
            p['breadcrumbs'].append({reverse('project', 
                args=[project.name,]): 'Projects'})
            p['slug'] = project.slug
            p['ideas'] = Idea.objects.filter(owner=req.user)
            for i in p['ideas']:
                if project in i.projects.all():
                    i.selected = True
            p['form'] = ProjectForm(instance=project)
            return render_to_response(TEMPLATE_PATH + 'project.html', p,
                context_instance=RequestContext(req))
        else:
          raise Http404
    elif req.method == 'POST':
        form = ProjectForm(req.POST)
        if form.is_valid():
            _save_project(form, project)
            ideas = req.POST.getlist('ideas', '')
            owned_idea_ids = Idea.objects.filter(owner=req.user, 
                id__in=ideas).values_list('id', flat=True).order_by('id')
            for i in ideas:
                # ensure this user came up with this idea
                if int(i) in owned_idea_ids:
                    idea = Idea.objects.get(id=i)
                    idea.projects.add(project)
                    idea.save()
            tags = req.POST.get('tags', '').strip()
            if tags != '':
                _add_tags(project, tags, req.user, 'project')
            messages.add_message(req, messages.INFO,
                'Project successfully updated.')
            return HttpResponseRedirect(reverse('projects'))
        else:
            p['form'] = form
            return render_to_response(TEMPLATE_PATH + 'project.html', p,
                context_instance=RequestContext(req))


def _save_project(form, p):
    p.name = form.cleaned_data['name']
    p.slug = _slugit(Project, p.name)
    p.repository_url = form.cleaned_data['repository_url']
    p.production_url = form.cleaned_data['production_url']
    p.save()

