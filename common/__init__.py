from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from taggit.models import Tag, TaggedItem
import json

def _json_response(dictionary):
    return HttpResponse(json.dumps(dictionary), mimetype='application/json')


def _slugit(cls, name):
    slug = slugify(name)
    count = 0
    while(cls.objects.filter(slug=slug).count() > 0):
        count += 1
        slug = slugify(name) + str(count)
    return slug


def _add_tags(obj, tags_str, creator, content_type_name):
    for tag_name in tags_str.split(','):
        tag_name = tag_name.strip()
        # don't recreate the tag if it already exists
        try:
            t = Tag.objects.get(slug=slugify(tag_name))
        except ObjectDoesNotExist as dne:
            t = Tag()
            t.name = tag_name[:99]
            t.slug = slugify(tag_name)
            t.save()
        ti = TaggedItem()
        ti.tag = t
        ti.object_id = obj.id
        ti.tag_creator = creator
        ti.content_type = ContentType.objects.filter(name=content_type_name)[0]
        ti.save()

