from django.test import TestCase, RequestFactory
from django.template import Context, Template
from tree_menu.models import Menu, MenuItem

class TreeMenuTests(TestCase):
    def setUp(self):
        # Создаём тестовое меню
        self.menu = Menu.objects.create(name="main_menu")
        self.home = MenuItem.objects.create(menu=self.menu, title="Home", url="/")
        self.about = MenuItem.objects.create(menu=self.menu, title="About", url="/about/")
        self.products = MenuItem.objects.create(menu=self.menu, title="Products", url="/products/")
        self.category1 = MenuItem.objects.create(menu=self.menu, title="Category 1", url="/products/1/", parent=self.products)

        self.factory = RequestFactory()

    def render_menu(self, path="/"):
        """Рендерим меню через template tag draw_menu"""
        request = self.factory.get(path)
        context = Context({"request": request})
        template = Template("{% load tree_menu_tags  %}{% draw_menu 'main_menu' %}")
        return template.render(context)

    def test_menu_renders_without_errors(self):
        """Меню рендерится без ошибок"""
        html = self.render_menu("/")
        self.assertIn("Home", html)
        self.assertIn("About", html)
        self.assertIn("Products", html)

    def test_active_item_highlighting(self):
        """Активный пункт меню определяется по URL"""
        html = self.render_menu("/products/")
        self.assertIn("Products", html)
        # Проверяем, что активный пункт как-то выделен
        self.assertIn("active", html)

    def test_submenu_expands_correctly(self):
        """Дочерние элементы Products отображаются при активном Products"""
        html = self.render_menu("/products/")
        self.assertIn("Category 1", html)

    def test_only_one_query_per_menu(self):
        """На одно меню должен быть один SQL-запрос"""
        from django.test.utils import CaptureQueriesContext
        from django.db import connection

        with CaptureQueriesContext(connection) as ctx:
            self.render_menu("/")
        self.assertLessEqual(len(ctx), 1, f"Too many DB queries: {len(ctx)}")

    def test_footer_menu_renders_independently(self):
        """Footer menu renders correctly and independently from main_menu"""
        # Создаем footer_menu и его пункты
        footer_menu = Menu.objects.create(name="footer_menu")
        MenuItem.objects.create(menu=footer_menu, title="Privacy", url="/privacy/")
        MenuItem.objects.create(menu=footer_menu, title="Terms", url="/terms/")

        # Рендерим footer_menu
        request = self.factory.get("/privacy/")
        context = Context({"request": request})
        template = Template("{% load tree_menu_tags %}{% draw_menu 'footer_menu' %}")
        html = template.render(context)

        # Проверяем, что пункты отображаются
        self.assertIn("Privacy", html)
        self.assertIn("Terms", html)

        # Проверяем, что main_menu не отображается
        self.assertNotIn("Home", html)
        self.assertNotIn("Products", html)
