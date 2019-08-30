# -*- coding: utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class HeroFile(models.Model):

    class Meta:
        verbose_name = u'фоновый медиафайл'
        verbose_name_plural = u'фоновые медиафайлы'

    OVERLAY_CHOICES = [
        ('0',  '0'), ('0.1', '10'), ('0.2', '20'), ('0.3', '30'), ('0.4', '40'), ('0.5', '50'),
        ('0.6', '60'), ('0.7', '70'), ('0.8', '80'), ('0.9', '90'), ('1', '100'),
    ]

    title = models.CharField(verbose_name=u'название', max_length=255)
    image = models.FileField(verbose_name=u'изображение', help_text=u'png, jpg', upload_to='upload')
    video = models.FileField(
        verbose_name=u'видеофайл', help_text=u'mp4',
        blank=True, null=True, upload_to='upload'
    )
    overlay_opacity = models.CharField(
        verbose_name=u'насыщенность эффекта затемнения',
        choices=OVERLAY_CHOICES, default='0.7', max_length=255
    )
    default = models.BooleanField(verbose_name=u'использовать по умолчанию', default=False)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(HeroFile, self).save(*args, **kwargs)
        if self.default:
            for hero in HeroFile.objects.filter(default=True).exclude(id=self.id):
                hero.default = False
                hero.save()


class HeroFileItem(models.Model):

    class Meta:
        verbose_name = u'фоновый медиафайл'
        verbose_name_plural = verbose_name

    show = models.BooleanField(verbose_name=u'отображать', default=True)
    herofile = models.ForeignKey(HeroFile, verbose_name=u'медафайл')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __unicode__(self):
        return u''
