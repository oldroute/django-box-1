# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Unit
from .forms import UnitAdminForm


@admin.register(Unit)
class UnitInline(admin.ModelAdmin):

    @property
    def media(self):
        media = super(UnitInline, self).media
        media.add_css({'all': ['css/admin/common.css']})
        return media

    model = Unit
    form = UnitAdminForm
    list_display = ('title', 'email')
