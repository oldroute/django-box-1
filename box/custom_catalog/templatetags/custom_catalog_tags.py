# -*- coding: utf-8 -*-
import json
from django import template
from django.core.cache import cache
from box.custom_catalog.models import Section, Product
from attachment.models import AttachmentImage
from django.contrib.contenttypes.models import ContentType
from box.links.models import Link
from catalog.utils import get_content_objects, get_sorted_content_objects
register = template.Library()


def get_sidebar_data(obj):

    """ Возвращает обьект сайдбара для кэширования """

    data, sections = [], []
    if isinstance(obj, Section):
        sections = get_sorted_content_objects(get_content_objects(obj.tree.get().get_siblings(include_self=True)))
    elif isinstance(obj, Product):
        sections = get_sorted_content_objects(get_content_objects(obj.tree.get().parent.get_siblings(include_self=True)))

    for section in sections:
        if isinstance(section, Section):
            data.append({
                'title': section.title,
                'get_absolute_url': section.get_absolute_url(),
                'current': section == obj
            })

    for link in Link.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, show=True):
        data.append({
            'title': link.text,
            'get_absolute_url': link.url,
        })

    return data


@register.inclusion_tag('parts/block_sidebar.html', takes_context=True)
def show_catalog_sidebar(context):

    """ Сайдбар содержит:
        - для драздела - разделы того же уровня + блок ссылок
        - для товара - разделы уровня родительского раздела + блок ссылок
    """

    obj = context.get('object')
    cache_key = 'sidebar-%d-%d' % (obj.tree.content_type.id, obj.id)
    json_data = cache.get(cache_key)
    if json_data:
        data = json.loads(json_data)
        # print '==FROM CACHE=>', cache_key
    else:
        data = get_sidebar_data(obj)
        cache.set(cache_key, json.dumps(data, ensure_ascii=False))
        # print '==SET CACHE=>', cache_key
    return {'object_list': data}


@register.inclusion_tag('catalog/parts/block_cards.html', takes_context=True)
def show_block_cards(context):
    obj = context.get('object')
    items = get_sorted_content_objects(get_content_objects(obj.tree.get().get_children()))
    sections, products = [], []
    for item in items:
        item_data = {
            'title': item.title,
            'get_absolute_url': item.get_absolute_url(),
            'description': item.description,
            'image': AttachmentImage.objects
                .filter(object_id=item.id, content_type=ContentType.objects.get_for_model(item)).first()
        }
        if item.leaf:
            item_data['produser'] = item.get_produser()
            products.append(item_data)
        else:
            sections.append(item_data)

    context['object_list'] = sections + products
    return context