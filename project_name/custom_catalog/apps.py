# -*- encoding: utf-8 -*-
from catalog.apps import CustomCatalogBaseConfig


class CustomCatalogAppConfig(CustomCatalogBaseConfig):
    name = '{{ project_name }}.custom_catalog'
    verbose_name = u'Модели каталога'

    def ready(self):
        super(CustomCatalogAppConfig, self).ready()
        from .signals import *
