# -*- coding: utf-8 -*-
from django.apps import AppConfig


class CustomFeedbackAppConfig(AppConfig):
    name = '{{ project_name }}.custom_feedback'
    verbose_name = u'Обратная связь'