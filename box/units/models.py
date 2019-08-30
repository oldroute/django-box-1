# -*- coding: utf-8 -*-
from django.db import models


class Unit(models.Model):

    class Meta:
        verbose_name = u'подразделение'
        verbose_name_plural = u'подразделения'

    show = models.BooleanField(verbose_name=u'отображать', default=True)
    title = models.CharField(verbose_name=u'наименование', max_length=255)
    email = models.EmailField(verbose_name=u'e-mail', max_length=255, help_text=u'Для рассылки с форм обратной связи')

    def __unicode__(self):
        return u'%s' % self.title
