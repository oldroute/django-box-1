# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import HeroFileItem, HeroFile
from .forms import HeroFileItemForm, HeroFileAdminForm


class HeroInline(GenericTabularInline):

    model = HeroFileItem
    extra = 1
    max_num = 1
    form = HeroFileItemForm


@admin.register(HeroFile)
class HeroFileAdmin(admin.ModelAdmin):

    @property
    def media(self):
        media = super(HeroFileAdmin, self).media
        media.add_css({'all': ['css/admin/common.css']})
        return media

    model = HeroFile
    form = HeroFileAdminForm
    list_display = ['title', 'default']
    list_editable = ['default']
