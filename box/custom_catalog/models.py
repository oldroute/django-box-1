# -*- encoding: utf-8 -*-
from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from tinymce.models import HTMLField
from pages.models import Page
from catalog.models import CatalogBase
from catalog.utils import get_content_objects, get_sorted_content_objects
from attachment.models import AttachmentImage
from django.contrib.contenttypes.models import ContentType


class Root(CatalogBase):
    class Meta:
        verbose_name = u'корневая страница'
        verbose_name_plural = verbose_name

    slug = ''
    title = models.CharField(verbose_name=u'название', max_length=400)
    long_title = models.CharField(verbose_name=u'длинное название', max_length=400, blank=True, null=True)
    main_content = HTMLField(verbose_name=u'контент в начале страницы', blank=True, null=True)
    bottom_content = HTMLField(verbose_name=u'контент в конце страницы', blank=True, null=True)

    last_modified = models.DateTimeField(auto_now=True)

    def get_menu_subsections(self, treeitem):
        data = {'col_1': [], 'col_2': []}
        ss = get_sorted_content_objects(get_content_objects(treeitem.get_children()))
        for i in range(len(ss)):
            if ss[i].__class__.__name__ == 'Section':
                ss_data = {
                    'title': ss[i].title,
                    'get_absolute_url': ss[i].get_absolute_url(),
                }
                data['col_2'].append(ss_data) if i % 2 else data['col_1'].append(ss_data)

        return data

    def get_menu_sections(self):
        data = []
        section_ct = ContentType.objects.get_for_model(Section)
        for obj in get_sorted_content_objects(get_content_objects(self.tree.get().get_children())):
            if obj.__class__.__name__ == 'Section':
                data.append({
                    'title': obj.title,
                    'get_absolute_url': obj.get_absolute_url(),
                    'children': self.get_menu_subsections(obj.tree.get()),
                    'image': AttachmentImage.objects
                        .filter(object_id=obj.id, content_type=section_ct).first()
                })
        return data

    def __unicode__(self, *args, **kwargs):
        return u'Корневая страница'

    def get_absolute_url(self):
        return reverse('catalog-root')


class Product(CatalogBase):
    class Meta:
        verbose_name = u'товар'
        verbose_name_plural = u'товары'

    leaf = True
    title = models.CharField(verbose_name=u'название', max_length=400)
    produser = models.ForeignKey(
        Page, limit_choices_to={'template': 'pages/produser.html', 'status': Page.PUBLISHED},
        verbose_name=u'производитель', null=True, blank=True
    )
    price = models.CharField(verbose_name=u'цена', max_length=255, blank=True, default='')
    vendor_code = models.CharField(verbose_name=u'артикул', max_length=255, blank=True, default='')
    description = models.TextField(verbose_name=u'короткое описание', default='', blank=True)
    main_content = HTMLField(verbose_name=u'основной контент', blank=True, null=True)
    content_1 = HTMLField(verbose_name=u'Характеристики', blank=True, null=True)
    content_2 = HTMLField(verbose_name=u'Описание', blank=True, null=True)

    def get_produser(self):
        if self.produser:
            return {
                'title': self.produser.title(),
                'get_absolute_url': self.produser.get_absolute_url(),
                'show_link': self.produser.status == Page.PUBLISHED
            }
        else:
            return None

    @property
    def images(self):
        return AttachmentImage.objects.filter(
            object_id=self.id,
            content_type=ContentType.objects.get_for_model(Product),
            role=settings.ROLE_GALLERY
        )

    def __unicode__(self):
        return self.title


class Section(CatalogBase):
    class Meta:
        verbose_name = u'раздел'
        verbose_name_plural = u'разделы'

    title = models.CharField(verbose_name=u'название', max_length=400)
    description = models.TextField(verbose_name=u'короткое описание', blank=True, null=True)
    main_content = HTMLField(verbose_name=u'основной контент', blank=True, null=True)
    bottom_content = HTMLField(verbose_name=u'контент в конце страницы', blank=True, null=True)

    @property
    def is_subsection(self):
        return bool(self.tree.get().level > 1)

    def __unicode__(self):
        return self.title
