from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from common import _add_tags, _slugit
from projects.models import Project
from ideas.models import Idea, ResearchLink
from ideas.forms import IdeaForm, ResearchLinkForm


TEMPLATE_PATH = 'ideas/'

def _create_params(req):
    p = {'breadcrumbs': [{reverse('ideas'): 'Ideas'}], 'is_ideas': True, 
        'nav_projects': Project.objects.filter( \
        owner=req.user).exclude(production_url__exact='')}
    p.update(csrf(req))
    return p


@login_required
def home(req):
    p = _create_params(req)
    p['ideas'] = Idea.objects.filter(owner=req.user).order_by('-created')
    p['research_links'] = ResearchLink.objects.filter(owner=req.user). \
        order_by('created')
    return render_to_response(TEMPLATE_PATH + 'home.html', p,
        context_instance=RequestContext(req))


@login_required
def new_idea(req):
    p = _create_params(req)
    p['breadcrumbs'].append({reverse('new_idea'): 'New Idea'})
    if req.method == 'GET':
        p['form'] = IdeaForm()
        return render_to_response(TEMPLATE_PATH + 'idea.html', p,
            context_instance=RequestContext(req))
    elif req.method == 'POST':
        form = IdeaForm(req.POST)
        if form.is_valid():
            idea = Idea()
            idea.owner = req.user
            _save_idea(form, idea)
            tags = req.POST.get('tags', '').strip()
            if tags != '':
                _add_tags(idea, tags, req.user, 'idea')
            messages.add_message(req, messages.INFO,
                'New idea "%s" successfully saved.' % idea.name)
            return HttpResponseRedirect(reverse('ideas'))
        else:
            p['form'] = form
            return render_to_response(TEMPLATE_PATH + 'idea.html', p,
                context_instance=RequestContext(req))

    
@login_required
def idea(req, slug):
    p = _create_params(req)
    p['idea'] = get_object_or_404(Idea, owner=req.user, slug=slug)
    p['slug'] = p['idea'].slug
    p['breadcrumbs'].append({reverse('idea', args=[slug,]): \
        p['idea'].name})
    if req.method == 'GET':
        p['form'] = IdeaForm(instance=p['idea'])
        return render_to_response(TEMPLATE_PATH + 'idea.html', p,
            context_instance=RequestContext(req))
    elif req.method == 'POST':
        idea = get_object_or_404(Idea, owner=req.user, slug=slug)
        form = IdeaForm(req.POST)
        if form.is_valid():
            _save_idea(form, idea)
            tags = req.POST.get('tags', '').strip()
            if tags != '':
                _add_tags(idea, tags, req.user, 'idea')
            messages.add_message(req, messages.INFO,
                'Idea "%s" successfully updated.' % idea.name)
            return HttpResponseRedirect(reverse('ideas'))
        else:
            p['form'] = form
            return render_to_response(TEMPLATE_PATH + 'idea.html', p,
                context_instance=RequestContext(req))


@login_required
def connections(req):
  p = _create_params(req)
  p['breadcrumbs'].append({reverse('idea_connections'): 'Connections'})
  p['ideas'] = Idea.objects.filter(owner=req.user).order_by('-created')
  return render_to_response(TEMPLATE_PATH + 'connections.html', p,
    context_instance=RequestContext(req))


@login_required
def new_research_link(req):
    p = _create_params(req)
    p['breadcrumbs'].append({reverse('new_research_link'): \
        'New Research Link'})
    if req.method == 'GET':
        p['form'] = ResearchLinkForm()
        return render_to_response(TEMPLATE_PATH + 'research_link.html', p,
            context_instance=RequestContext(req))
    elif req.method == 'POST':
        form = ResearchLinkForm(req.POST)
        if form.is_valid():
            link = ResearchLink()
            link.owner = req.user
            _save_research_link(form, link)
            tags = req.POST.get('tags', '').strip()
            if tags != '':
                _add_tags(link, tags, req.user, 'research link')
            messages.add_message(req, messages.INFO,
                'New research link "%s" created successfully.' % link.name)
            return HttpResponseRedirect(reverse('ideas'))
        else:
            p['form'] = form
            return render_to_response(TEMPLATE_PATH + 'research_link.html', p,
                context_instance=RequestContext(req))


@login_required
def research_link(req, slug=''):
    p = _create_params(req)
    p['link'] = get_object_or_404(ResearchLink, owner=req.user, slug=slug)
    p['breadcrumbs'].append({'ideas/link/%s/' % slug: p['link'].name })
    p['slug'] = p['link'].slug
    if req.method == 'GET':
        p['form'] = ResearchLinkForm(instance=p['link'])
        return render_to_response(TEMPLATE_PATH + 'research_link.html', p,
            context_instance=RequestContext(req))
    elif req.method == 'POST':
        form = ResearchLinkForm(req.POST)
        if form.is_valid():
            link = p['link']
            link.owner = req.user
            _save_research_link(form, link)
            messages.add_message(req, messages.INFO,
                'Research link  "%s" successfully updated.' % link.name)
            return HttpResponseRedirect(reverse('ideas'))
        else:
            p['form'] = form
            return render_to_response(TEMPLATE_PATH + 'research_link.html', p,
                context_instance=RequestContext(req))


@login_required
def add_idea_to_connection(req):
    p = _create_params(req)
    return HttpResponse('ok')


def _save_idea(form, i):
    i.name = form.cleaned_data['name']
    i.slug = _slugit(Idea, i.name)
    i.concept = form.cleaned_data['concept']
    i.save()


def _save_research_link(form, l):
    l.name = form.cleaned_data['name']
    l.slug = _slugit(ResearchLink, l.name)
    l.link_url = form.cleaned_data['link_url']
    l.save()

