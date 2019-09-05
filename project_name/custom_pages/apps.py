# -*- encoding: utf-8 -*-
from django.apps import AppConfig


class CustomPagesAppConfig(AppConfig):
    name = '{{ project_name }}.custom_pages'

    def ready(self):
        from . import widgets, signals