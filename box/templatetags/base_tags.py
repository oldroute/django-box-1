# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils.html import strip_spaces_between_tags
from attachment.models import AttachmentImage
from easy_news.models import News
from django.contrib.contenttypes.models import ContentType
from box.links.models import Link
from box.service.models import SiteSettings

try:
    NEWS_CT = ContentType.objects.get_for_model(News)
except:
    pass

register = template.Library()


@register.inclusion_tag('parts/block_content.html')
def show_block_content(content):

    """ Отображение блока html-контента """

    return {'content': content}


@register.assignment_tag(takes_context=True)
def get_hero_image(context):
    obj = context.get('object', context.get('current_page'))
    if obj:
        return AttachmentImage.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, group__iexact=u'фон').first()
    else:
        return AttachmentImage.objects.None()


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
            'image': AttachmentImage.objects.filter(object_id=obj.id, content_type=NEWS_CT).first()
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


def get_ranged_pagination_pages(current, pages, count):

    """ Возвращает список из count страниц пагинации вокруг текущего элемента
        count - четное кол-во элементов пагинации """

    result = pages
    if len(pages):
        first_page, last_page = pages[0], pages[-1]
        if count < last_page:
            step = count / 2
            left_page = current - step + 1
            right_page = current + step
            if left_page < first_page and right_page > last_page:
                pass
            elif left_page < first_page:
                right_page += (first_page - left_page)
                if right_page > last_page:
                    right_page = last_page
                left_page = first_page
            elif right_page > last_page:
                left_page -= right_page - last_page
                if left_page < first_page:
                    left_page = first_page
                right_page = last_page

            result = [i for i in range(left_page, right_page + 1)]
    return result


@register.assignment_tag
def get_custom_pagination(current, pages):

    """ Возвращает объект пагинации"""

    data = {}
    data['pages'] = get_ranged_pagination_pages(current, pages, count=4)
    data['first'] = 1
    data['last'] = pages[-1]
    data['prev'] = data['pages'][0] - 1
    if data['prev'] < data['first']:
        data['prev'] = None
    data['next'] = data['pages'][-1] + 1
    if data['next'] > data['last']:
       data['next'] = None
    return data


@register.assignment_tag(takes_context=True)
def get_menu_items(context):

    """ Разделить пункты главного меню на 2 части """

    menu = context.get('menu')
    items = []
    for item in menu.root_item.children():
        if item.show:
            items.append(item)

    right = [items[i] for i in range(len(items)/2)]
    left = [items[i] for i in range(len(right), len(items))]
    return {
        'left': left,
        'right': right
    }


@register.assignment_tag
def get_fp_logo_url():

    """ Получение url логотипа на главной странице """

    img = '/static/img/fp-logo.svg'
    site_settings = SiteSettings.objects.filter(site_ptr=settings.SITE_ID).first()
    if site_settings and site_settings.fp_logo:
        img = site_settings.fp_logo.url
    return img


@register.assignment_tag(takes_context=True)
def get_admin_sidebar_models(context):

    """ Получить список ссылок для сайдбара в админке """

    user = context['request'].user
    data = []
    if user.is_superuser or user.has_perm('service.change_sitesettings'):
        data.append({'title': u'Настройки домена', 'url': '/admin/service/sitesettings/'})
    if user.is_superuser or user.has_perm('service.change_errorpage'):
        data.append({'title': u'Страницы ошибок', 'url': '/admin/service/errorpage/'})
    if user.is_superuser or user.has_perm('auth.add_user') or user.has_perm('auth.change_user'):
        data.append({'title': u'Пользователи', 'url': '/admin/auth/user/'})
    if user.is_superuser or user.has_perm('auth.add_group') or user.has_perm('auth.change_group'):
        data.append({'title': u'Группы', 'url': '/admin/auth/group/'})
    return data


class SmartSpacelessNode(template.Node):

    """ Удалить пробелы из шаблона если отключен режим отладки """

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        return content if  settings.DEBUG else strip_spaces_between_tags(content.strip())


@register.tag
def smart_spaceless(parser, token):

    nodelist = parser.parse(('end_smart_spaceless',))
    parser.delete_first_token()
    return SmartSpacelessNode(nodelist)