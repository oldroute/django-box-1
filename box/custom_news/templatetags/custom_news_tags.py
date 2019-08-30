# -*- coding: utf-8 -*-
from django import template
from attachment.models import AttachmentImage
from easy_news.models import News
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from box.links.models import Link
from box.custom_news.models import NewsRoot

try:
    NEWS_CT = ContentType.objects.get_for_model(News)
except:
    pass

register = template.Library()


@register.inclusion_tag('easy_news/parts/block_cards.html', takes_context=True)
def show_block_news(context):

    """ Отображает блок новостей """

    context['object_list'] = []
    for obj in News.objects.filter(show=True):
        context['object_list'].append({
            'title': obj.title,
            'date': obj.date,
            'short_description': obj.short_description,
            'get_absolute_url': obj.get_absolute_url(),
            'image': AttachmentImage.objects
                .filter(object_id=obj.id, content_type=NEWS_CT).first()
        })
    return context


@register.inclusion_tag('parts/block_sidebar.html', takes_context=True)
def show_news_sidebar(context):

    """ Сайдбар новостей содержит только блок ссылок """

    data = []
    obj = context.get('object')
    for link in Link.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, show=True):
        data.append({
            'title': link.text,
            'get_absolute_url': link.url,
        })

    return {'object_list': data}


@register.simple_tag
def news_root_admin_link():

    """ Ссылка на корневую страницу новостей для страницы списка новостей """

    obj = NewsRoot.objects.all().first()
    if not obj:
        obj = NewsRoot.objects.create(title=u'Новости')
    return reverse('admin:custom_news_newsroot_change', args=[obj.id])


@register.assignment_tag()
def get_news_root():
    return NewsRoot.objects.all().first()