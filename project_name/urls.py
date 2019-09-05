# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from pages import views as pages_views
from filebrowser.sites import site


urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^', include('attachment.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^news/', include('{{ project_name }}.custom_news.urls')),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^', include('{{ project_name }}.service.urls')),
    url(r'^(?P<path>.*)/$', pages_views.details, name='pages-details-by-path'),
    url(r'^$', pages_views.details, name='pages-root', kwargs={'path': u''})
]

if settings.DEBUG:
    urlpatterns = [
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


handler404 = '{{ project_name }}.service.views.handler404'
handler500 = '{{ project_name }}.service.views.handler500'

try:
    from {{ project_name }}.service.models import SiteSettings
    site_settings = SiteSettings.objects.all().first()
    if site_settings:
        admin.site.site_header = site_settings.name
except:
    pass
