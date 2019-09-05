# -*- coding:utf-8 -*-
from django.contrib import admin
from catalog.admin import CatalogItemBaseAdmin
from .models import Section, Product, Root
from .forms import ProductAdminForm, SectionAdminForm, RootAdminForm


@admin.register(Root)
class RootAdmin(CatalogItemBaseAdmin):

    @property
    def media(self):
        media = super(RootAdmin, self).media
        media.add_css({'all': ['css/admin/common.css']})
        return media

    def has_add_permission(self, request):
        return not bool(Root.objects.exists())

    def has_delete_permission(self, request, obj=None):
        return False

    model = Root
    form = RootAdminForm
    fields = ['title', 'long_title', 'main_content', 'bottom_content']


@admin.register(Product)
class ProductAdmin(CatalogItemBaseAdmin):

    @property
    def media(self):
        media = super(ProductAdmin, self).media
        media.add_css({'all': ['css/admin/common.css']})
        return media

    model = Product
    form = ProductAdminForm
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", )
    fields = ['title', 'slug', 'show', 'price', 'description', 'main_content']


@admin.register(Section)
class SectionAdmin(CatalogItemBaseAdmin):

    @property
    def media(self):
        media = super(SectionAdmin, self).media
        media.add_css({'all': ['css/admin/common.css']})
        return media

    model = Section
    form = SectionAdminForm
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", )
    fields = ['title', 'slug', 'show', 'description', 'main_content', 'bottom_content']

