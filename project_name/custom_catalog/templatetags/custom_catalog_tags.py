# -*- coding: utf-8 -*-
from django import template
from attachment.models import AttachmentImage
from django.contrib.contenttypes.models import ContentType
from catalog.utils import get_content_objects, get_sorted_content_objects


register = template.Library()


@register.inclusion_tag('catalog/parts/block_cards.html', takes_context=True)
def show_block_cards(context):

    """ Возвращает список разделов + список товаров """

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
            products.append(item_data)
        else:
            sections.append(item_data)

    context['object_list'] = sections + products
    return context