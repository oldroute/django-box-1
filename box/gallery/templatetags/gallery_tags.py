# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.html import mark_safe
from box.gallery.models import HeroFileItem, HeroFile

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_hero(context):

    """ Если для страницы не выбран фоновый медиафайл - возвращается дефолтный """

    obj = context.get('object', context.get('current_page'))
    hero = None
    if obj:
        hero_item = HeroFileItem.objects.filter(show=True, content_type=ContentType.objects.get_for_model(obj), object_id=obj.id).first()
        if hero_item:
            hero = hero_item.herofile
    if not hero:
        hero = HeroFile.objects.filter(default=True).first()
    return hero
