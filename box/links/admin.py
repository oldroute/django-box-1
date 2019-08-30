# -*- coding: utf-8 -*-
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Link


class LinkInline(GenericTabularInline):
    model = Link
    extra = 0
    fields = ('order_key', 'show', 'text', 'url')
