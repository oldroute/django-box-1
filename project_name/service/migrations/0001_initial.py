# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-30 10:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[(b'404', b'404'), (b'500', b'500')], max_length=255, verbose_name='\u0442\u0438\u043f')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('main_content', tinymce.models.HTMLField(blank=True, null=True, verbose_name='\u043a\u043e\u043d\u0442\u0435\u043d\u0442')),
            ],
            options={
                'verbose_name': '\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u043e\u0448\u0438\u0431\u043a\u0438',
                'verbose_name_plural': '\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b \u043e\u0448\u0438\u0431\u043e\u043a',
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('site_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sites.Site')),
                ('robots', models.TextField(blank=True, default='user-agent: *\ndisallow: /', null=True, verbose_name='\u0441\u043e\u0434\u0435\u0440\u0436\u0438\u043c\u043e\u0435 \u0444\u0430\u0439\u043b\u0430 robots.txt')),
                ('fp_logo', models.FileField(blank=True, help_text='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 204 x 204 px (jpeg, jpg, png, svg).<br> \u0415\u0441\u043b\u0438 \u043d\u0435 \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u043e - \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0435\u0442\u0441\u044f \u043b\u043e\u0433\u043e\u0442\u0438\u043f \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e', null=True, upload_to=b'upload', verbose_name='\u041b\u043e\u0433\u043e\u0442\u0438\u043f \u0434\u043b\u044f \u0433\u043b\u0430\u0432\u043d\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b')),
            ],
            options={
                'verbose_name': '\u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0434\u043e\u043c\u0435\u043d\u0430',
                'verbose_name_plural': '\u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0434\u043e\u043c\u0435\u043d\u0430',
            },
            bases=('sites.site',),
        ),
    ]