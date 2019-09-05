# -*- encoding: utf-8 -*-
from django.apps import AppConfig


class CustomNewsAppConfig(AppConfig):
    name = '{{ project_name }}.custom_news'
    verbose_name = u'Новости'
