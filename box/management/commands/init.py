# -*- coding: utf-8 -*-
import sys
from django.core.management.base import BaseCommand, CommandError
from chunks.models import Chunk
from treemenus.models import MenuItem, Menu
from pages.models import Page, Content
from easy_news.models import News
from django.contrib.auth import get_user_model
from django.db import transaction
from django.conf import settings
from django.contrib.sites.models import Site
from catalog.models import TreeItem
from box.service.models import SiteSettings
from box.custom_catalog.models import Product, Section, Root
from box.custom_news.models import NewsRoot
from ..utils import GUIDELINE_CONTENT, BLOCK_CONTENT, BLOCK_DESC


UserModel = get_user_model()


class Command(BaseCommand):

    help = 'Create initial data'

    def _create_site(self):
        sys.stdout.write("\rCreating site...")
        site_settings = SiteSettings.objects.filter(site_ptr=settings.SITE_ID).first()
        if not site_settings:
            default_site = Site.objects.filter(id=settings.SITE_ID).first()
            site_settings = SiteSettings.objects.create(site_ptr=default_site)
            site_settings.domain = site_settings.name = 'localhost:8000'
            site_settings.save()
            sys.stdout.write(self.style.SUCCESS("           OK\n"))
        else:
            sys.stdout.write(self.style.WARNING("           ALREADY EXIST\n"))

    def _create_superuser(self):
        username = password = '1'
        email = '1@m.ru'
        sys.stdout.write("\rCreating superuser...")

        try:
            user = UserModel.objects.get(username=username, email=email)
            sys.stdout.write(self.style.WARNING("      ALREADY EXIST\n"))
        except:
            user = UserModel.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_active=True,
                is_superuser=True,
            )
            sys.stdout.write(self.style.SUCCESS("      OK\n"))
        sys.stdout.write(self.style.SUCCESS('\rusername: %s\n\rpassword: %s\n' % (username, password)))

    def _create_chunks(self):
        sys.stdout.write("\rCreating chunks...")
        try:
            with transaction.atomic():
                Chunk.objects.bulk_create([
                    Chunk(key='description', description=u'Подпись к логотипу в шапке', content=u''),
                    Chunk(key='description_footer', description=u'Подпись к логотипу в подвале', content=u''),
                    Chunk(key='privacy_policy', description=u'Формы: текст согласия с политкой конфиденциальности',
                          content=u''),

                    Chunk(key='name', description=u'Организация: название', content=u''),
                    Chunk(key='working_hours', description=u'Организация: часы работы', content=u''),
                    Chunk(key='phone', description=u'Организация: телефон', content=u''),
                    Chunk(key='email', description=u'Организация: e-mail', content=u''),

                    Chunk(key='yandex_search_form', description=u'Yandex-поиск: скрипт формы', content=u''),
                    Chunk(key='yandex_search_results', description=u'Yandex-поиск: скрипт результатов поиска', content=u''),

                    Chunk(key='address_postal_code', description=u'Адрес: почтовый индекс', content=u''),
                    Chunk(key='address_city', description=u'Адрес: город', content=u''),
                    Chunk(key='address_street_and_home', description=u'Адрес: улица, дом', content=u''),

                    Chunk(key='developer_url', description=u'Разработчик: ссылка на сайт', content=u''),
                    Chunk(key='developer_slogan', description=u'Разработчик: подпись к логотипу', content=u''),

                    Chunk(key='end_of_head', description=u'Блок контента перед </head>', content=u''),
                    Chunk(key='top_of_body', description=u'Блок контента после <body>', content=u''),
                    Chunk(key='end_of_body', description=u'Блок контента перед </body>', content=u''),
                ])
            sys.stdout.write(self.style.SUCCESS("         OK\n"))
        except:
            sys.stdout.write(self.style.WARNING("         ALREADY EXIST\n"))

    def _create_menus(self):

        # Circle menu
        sys.stdout.write("\rCreating circle_menu...")
        try:
            circle_menu = Menu.objects.get(name='circle_menu')
            sys.stdout.write(self.style.WARNING("    ALREADY EXIST\n"))
        except:
            with transaction.atomic():
                circle_menu = Menu.objects.create(name='circle_menu')
                MenuItem.objects.bulk_create([
                    MenuItem(menu=circle_menu, parent=circle_menu.root_item, caption=u'Компания', url='/'),
                    MenuItem(menu=circle_menu, parent=circle_menu.root_item, caption=u'Аренда', url='/'),
                    MenuItem(menu=circle_menu, parent=circle_menu.root_item, caption=u'Складские услуги', url='/'),
                    MenuItem(menu=circle_menu, parent=circle_menu.root_item, caption=u'Транспортные услуги', url='/'),
                    MenuItem(menu=circle_menu, parent=circle_menu.root_item, caption=u'Продукция', url='/'),
                    MenuItem(menu=circle_menu, parent=circle_menu.root_item, caption=u'Информация для акционеров', url='/'),
                    MenuItem(menu=circle_menu, parent=circle_menu.root_item, caption=u'Контакты', url='/'),
                    MenuItem(menu=circle_menu, parent=circle_menu.root_item, caption=u'Карьера', url='/'),
                ])
            sys.stdout.write(self.style.SUCCESS("    OK\n"))

        # Header menu
        sys.stdout.write("\rCreating header_menu...")
        try:
            header_menu = Menu.objects.get(name='header_menu')
            sys.stdout.write(self.style.WARNING("    ALREADY EXIST\n"))
        except:
            with transaction.atomic():
                header_menu = Menu.objects.create(name='header_menu')
                _ = MenuItem.objects.create(menu=header_menu, parent=header_menu.root_item, caption=u'Новости', url='/news/')
                _ = MenuItem.objects.create(menu=header_menu, parent=header_menu.root_item, caption=u'Каталог', url='/catalog/')
                _ = MenuItem.objects.create(menu=header_menu, parent=header_menu.root_item, caption=u'Очень длинный пункт меню', url='/')
                _ = MenuItem.objects.create(menu=header_menu, parent=header_menu.root_item, caption=u'Короткий', url='/')
                _ = MenuItem.objects.create(menu=header_menu, parent=header_menu.root_item, caption=u'Пункт меню', url='/')

                menu_item = MenuItem.objects.create(menu=header_menu, parent=header_menu.root_item, caption=u'Содержит подпункты', url='/')
                _ = MenuItem.objects.create(menu=header_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=header_menu, parent=menu_item, caption=u'Очень длинный пункт меню', url='/')
                _ = MenuItem.objects.create(menu=header_menu, parent=menu_item, caption=u'Короткий', url='/')
                _ = MenuItem.objects.create(menu=header_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=header_menu, parent=menu_item, caption=u'Пункт меню', url='/')

            sys.stdout.write(self.style.SUCCESS("    OK\n"))

        # Footer menu
        sys.stdout.write("\rCreating footer_menu...")
        try:
            footer_menu = Menu.objects.get(name='footer_menu')
            sys.stdout.write(self.style.WARNING("    ALREADY EXIST\n"))
        except:
            with transaction.atomic():
                footer_menu = Menu.objects.create(name='footer_menu')
                menu_item = MenuItem.objects.create(menu=footer_menu, parent=footer_menu.root_item, caption=u'Футер меню 1', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Очень длинный пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Короткий', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Пункт меню', url='/')

                menu_item = MenuItem.objects.create(menu=footer_menu, parent=footer_menu.root_item, caption=u'Футер меню 2', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Очень длинный пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Короткий', url='/')

                menu_item = MenuItem.objects.create(menu=footer_menu, parent=footer_menu.root_item, caption=u'Футер меню 3', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Короткий', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Очень длинный пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Очень длинный пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Очень длинный пункт меню', url='/')
                _ = MenuItem.objects.create(menu=footer_menu, parent=menu_item, caption=u'Короткий', url='/')

            sys.stdout.write(self.style.SUCCESS("    OK\n"))

        # Social menu
        sys.stdout.write("\rCreating social_menu...")
        try:
            social_menu = Menu.objects.get(name='social_menu')
            sys.stdout.write(self.style.WARNING("    ALREADY EXIST\n"))
        except:
            with transaction.atomic():
                social_menu = Menu.objects.create(name='social_menu')
                _ = MenuItem.objects.create(menu=social_menu, parent=social_menu.root_item, caption=u'vkontakte', url='/')
                _ = MenuItem.objects.create(menu=social_menu, parent=social_menu.root_item, caption=u'facebook', url='/')
                _ = MenuItem.objects.create(menu=social_menu, parent=social_menu.root_item, caption=u'twitter', url='/')
                _ = MenuItem.objects.create(menu=social_menu, parent=social_menu.root_item, caption=u'youtube', url='/')
            sys.stdout.write(self.style.SUCCESS("    OK\n"))

    def _create_pages(self):
        # Guideline page
        sys.stdout.write("\rCreating default page...")
        default_page = Page.objects.filter(template='pages/default.html', status=Page.PUBLISHED).first()
        if default_page:
            sys.stdout.write(self.style.WARNING("   ALREADY EXIST\n"))
        else:
            default_page = Page.objects.create(
                template='pages/default.html',
                status=Page.PUBLISHED,
                author=UserModel.objects.get(username='1', email='1@m.ru')
            )
            Content.objects.create(
                page=default_page, language=settings.LANGUAGE_CODE,
                type='title', body=u'Гайдлайн'
            )
            Content.objects.create(
                page=default_page, language=settings.LANGUAGE_CODE,
                type='slug', body=u'guidelines'
            )
            Content.objects.create(
                page=default_page,
                language=settings.LANGUAGE_CODE,
                type='main_content',
                body=GUIDELINE_CONTENT,
            )
            sys.stdout.write(self.style.SUCCESS("   OK\n"))

    def _create_news(self):
        sys.stdout.write("\rCreating news...")
        root = NewsRoot.objects.all().first()
        if not root:
            root = NewsRoot.objects.create(title=u'Новости', main_content=BLOCK_CONTENT, bottom_content=BLOCK_CONTENT)
        if not root.news.exists():
            for i in range(21):
                News.objects.create(title=u'Новость %d' % i, slug='news-%d' % i, author=u'Феофан Матвеев', short=BLOCK_DESC,  text=BLOCK_CONTENT),
            sys.stdout.write(self.style.SUCCESS("           OK\n"))
        else:
            sys.stdout.write(self.style.WARNING("           ALREADY EXIST\n"))

    def _create_catalog(self):
        sys.stdout.write("\rCreating catalog...")
        root_page = Root.objects.all().first()
        if not root_page:
            root_page = Root.objects.create(title=u'Каталог', main_content=BLOCK_CONTENT, bottom_content=BLOCK_CONTENT)
            TreeItem.objects.create(content_object=root_page)
        root = root_page.tree.get()
        if not root.get_children().exists():
            for i in range(1, 8):
                section = Section.objects.create(title=u'Раздел %d' % i, slug='section-%d' % i, main_content=BLOCK_CONTENT)
                section.tree.get().move_to(root)
            for i in range(1, 17):
                Product.objects.create(title=u'Товар %d' % i, slug='product-%d' % i, main_content=BLOCK_CONTENT)

            section_1 = Section.objects.get(id=1).tree.get()
            for ss in Section.objects.filter(id__in=[2, 3, 4]):
                ss.tree.get().move_to(section_1)

            section_2 = Section.objects.get(id=2).tree.get()
            for p in Product.objects.filter(id__in=[1, 2, 3, 4, 5]):
                p.tree.get().move_to(section_2)

            section_3 = Section.objects.get(id=3).tree.get()
            for p in Product.objects.filter(id__in=[6, 7, 8, 9, 10]):
                p.tree.get().move_to(section_3)

            section_5 = Section.objects.get(id=5).tree.get()
            section_6 = Section.objects.get(id=6).tree.get()
            section_6.move_to(section_5)
            Product.objects.get(id=11).tree.get().move_to(section_6)

            section_7 = Section.objects.get(id=7).tree.get()
            for p in Product.objects.filter(id__in=[12, 13, 14, 15, 16]):
                p.tree.get().move_to(section_7)


            sys.stdout.write(self.style.SUCCESS("        OK\n"))
        else:
            sys.stdout.write(self.style.WARNING("        ALREADY EXIST\n"))

    def handle(self, *args, **options):
        self._create_superuser()
        self._create_site()
        self._create_chunks()
        self._create_menus()
        self._create_pages()
        self._create_news()
        self._create_catalog()
