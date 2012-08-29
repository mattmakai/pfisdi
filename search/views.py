import re

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from ideas.models import Idea, ResearchLink
from projects.models import Project
from taggit.models import Tag

TEMPLATE_PATH = 'search/'

@csrf_protect
@login_required
def tag_search(req, term=''):
    if req.method == 'POST':
        term = req.POST.get('search', '').strip()
        return HttpResponseRedirect(reverse('search', args=[term,]))
    elif req.method == 'GET':
        entry_query = get_query(term, ['name',])
        tag_pks = Tag.objects.filter( \
            name__contains=term).values_list('pk', flat=True)
        matching_tags = Tag.objects.filter(pk__in=tag_pks)
        ideas = Idea.objects.filter(tags__pk__in=tag_pks).distinct()
        links = ResearchLink.objects.filter(tags__pk__in=tag_pks).distinct()
        projects = Project.objects.filter(tags__pk__in=tag_pks).distinct()
        p = {'query_string': term, 'found_ideas': ideas, 
            'found_links': links, 'found_projects': projects, 
            'matching_tags': matching_tags,
            'breadcrumbs': [{reverse('tag_search', args=[term,]): \
            'Search Results'}]}
        return render_to_response(TEMPLATE_PATH + 'search_results.html', p, 
            context_instance=RequestContext(req))


def _get_query(query_string, search_fields):
    query = None
    terms = _normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def _normalize_query(query_string, \
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall, \
    normspace=re.compile(r'\s{2,}').sub):
    """
        Splits the query string in individual keywords, getting rid of 
        unnecessary spaces and grouping quotes words together.
    """
    return [normspace(' ', (t[0] or t[1]).strip()) \
        for t in findterms(query_string)]


