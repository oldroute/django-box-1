# -*- coding: utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Link(models.Model):

    class Meta:
        verbose_name = u'пункт меню'
        verbose_name_plural = u'пункты меню в сайдбаре'
        ordering = ['order_key']

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    order_key = models.IntegerField(verbose_name=u'порядок', null=True, blank=True)
    show = models.BooleanField(verbose_name=u'отображать', default=True)
    text = models.CharField(verbose_name=u'текст', max_length=255)
    url = models.CharField(verbose_name=u'url', max_length=255)

    def save(self, *args, **kwargs):
        if self.order_key is None:
            self.order_key = Link.objects.filter(object_id=self.object_id, content_type=self.content_type).aggregate(models.Count('id'))["id__count"] + 1
        super(Link, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.text
