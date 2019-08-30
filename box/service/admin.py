# -*- coding utf-8 -*-
from django.contrib import admin
from django.contrib.sites.admin import Site
from .models import ErrorPage, SiteSettings
from .forms import ErrorPageAdminForm, SiteSettingsAdminForm
from box.gallery.admin import HeroInline


@admin.register(ErrorPage)
class ErrorPageAdmin(admin.ModelAdmin):

    @property
    def media(self):
        media = super(ErrorPageAdmin, self).media
        media.add_css({'all': ['css/admin/common.css']})
        return media

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.save()
        obj.generate_static_page(request)

    model = ErrorPage
    form = ErrorPageAdminForm
    list_display = ('type', 'title')
    inlines = [HeroInline]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    @property
    def media(self):
        media = super(SiteSettingsAdmin, self).media
        media.add_css({'all': ['css/admin/common.css']})
        return media

    model = SiteSettings
    form = SiteSettingsAdminForm

    def save_model(self, request, obj, form, change):
        obj.generate_robots_file()
        obj.save()

try:
    admin.site.unregister(Site)
except:
    pass