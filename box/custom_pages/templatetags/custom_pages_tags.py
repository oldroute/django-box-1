# -*- coding: utf-8 -*-
import json
from django.core.cache import cache
from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from collections import OrderedDict
from attachment.models import AttachmentImage
from pages.models import Page
from box.links.models import Link
from box.custom_catalog.models import Product


register = template.Library()
try:
    PAGE_CT = ContentType.objects.get_for_model(Page)
    PRODUCT_CT = ContentType.objects.get_for_model(Product)
    LANG = settings.LANGUAGE_CODE
except:
    pass


@register.inclusion_tag('pages/parts/block_gallery.html', takes_context=True)
def show_block_gallery(context, key='all'):

    """  Отображает блок-галерею """

    obj = context.get("current_page")
    images = AttachmentImage.objects.filter(object_id=obj.id, content_type_id=PAGE_CT, role=settings.ROLE_GALLERY)
    # если не нужно выводить изображения без групп
    if key == "grouped_only":
        images = images.exclude(group="").exclude(group=None)
    images = images.order_by("group", "position")

    grouped_images = OrderedDict()
    if images.exists():
        groups = images.order_by("group").values_list("group", flat=True)
        empty_group_images = []
        for group in groups:
            if group:
                grouped_images[group] = []
        for image in images:
            if image.group:
                grouped_images[image.group].append(image)
            else:
                empty_group_images.append(image)

        if empty_group_images:
            grouped_images[None] = empty_group_images

    context["object_dict"] = grouped_images
    return context


@register.inclusion_tag('pages/parts/block_cards.html', takes_context=True)
def show_block_cards(context):
    context['object_list'] = []
    obj = context.get("current_page")

    for page in obj.get_children().filter(status=Page.PUBLISHED):

        context['object_list'].append({
            'title': page.title(),
            'description': page.get_content(LANG, 'description'),
            'image': AttachmentImage.objects
                .filter(object_id=page.id, content_type=PAGE_CT).first(),
            'get_absolute_url': page.get_absolute_url()
        })
    return context


def get_children_data(page, current_page):

    """ Возвращает обьект с данными дочерней страницы для сайдбара """

    data = []
    hide_child_pages_from_sidebar = page.get_content(settings.LANGUAGE_CODE, 'hide_child_pages_from_sidebar') or 'False'
    if hide_child_pages_from_sidebar == 'False':
        for page in page.get_children().filter(status=Page.PUBLISHED):
            hide_from_sidebar = page.get_content(settings.LANGUAGE_CODE, 'hide_from_sidebar') or 'False'
            if hide_from_sidebar == 'False':
                item = {
                    'title': page.title(),
                    'get_absolute_url': page.get_absolute_url(),
                }
                if current_page.get_absolute_url() == page.get_absolute_url():
                    item['current'] = True
                data.append(item)
    return data


def get_sidebar_data(current_page):

    """ Возвращает обьект сайдбара для кэширования """

    data = []
    for page in current_page.get_siblings(include_self=True).filter(status=Page.PUBLISHED).exclude(template='pages/frontpage.html'):
        hide_from_sidebar = page.get_content(settings.LANGUAGE_CODE, 'hide_from_sidebar') or 'False'
        if hide_from_sidebar == 'False':
            item = {
                'title': page.title(),
                'get_absolute_url': page.get_absolute_url(),
            }
            children = get_children_data(page, current_page)
            if children:
                item['children'] = children
            if current_page.get_absolute_url() == page.get_absolute_url():
                item['current'] = True
            if current_page.get_absolute_url() == page.get_absolute_url() and children:
                item['toggle'] = True
            data.append(item)

    for link in Link.objects.filter(content_type=ContentType.objects.get_for_model(current_page), object_id=current_page.id, show=True):
        data.append({
            'title': link.text,
            'get_absolute_url': link.url,
        })
    # Исключить случай когда в сайдбаре отображаеться только текущая страница
    if len(data) == 1 and data[0]['get_absolute_url'] == current_page.get_absolute_url():
        data.pop()

    return data


@register.inclusion_tag('parts/block_sidebar.html', takes_context=True)
def show_sidebar(context):

    """ Сайдбар страницы содержит смежные страницы и блок ссылок """

    obj = context.get('current_page')
    cache_key = 'sidebar-%d-%d' % (PAGE_CT.id, obj.id)
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
def show_block_products(context):
    obj = context.get('current_page')
    data = []
    for product in Product.objects.filter(produser=obj, show=True).order_by('tree'):
        data.append({
            'title': product.title,
            'get_absolute_url': product.get_absolute_url(),
            'description': product.description,
            'image': AttachmentImage.objects
                .filter(content_type=PRODUCT_CT, object_id=product.id).first(),
            'produser': product.get_produser()
        })
    context.update({'object_list': data})
    return context