import json

from django.urls import reverse
from django.test import TestCase
from random import choices
from string import ascii_letters
from shopapp.models import Product, Order
from django.contrib.auth.models import User
from django.conf import settings


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()
        self.user = User.objects.create_user(username='myusername', password='mypassword')
        self.user.save()
        self.user.user_permissions.add(25)
        self.client.login(username='myusername', password='mypassword')
    def test_product_create(self):

        response = self.client.post(
            reverse("shopapp:create-product"),
            {"name": self.product_name,
             "price": "1234",
             "description": "good",
             "discount": "15",
             },
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())

class ProductDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='myusername', password='mypassword', is_superuser=True)
        cls.user.save()
        cls.product = Product.objects.create(name="".join(choices(ascii_letters, k=10)), created_by=cls.user)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.product.delete()
        cls.user.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:products_detail", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_context(self):
        response = self.client.get(
            reverse("shopapp:products_detail", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):

    fixtures = [
        "products-fixture.json",
    ]
    def test_product(self):
        response = self.client.get(
            reverse("shopapp:products_list")
        )

        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,

        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='myusername', password='mypassword')
        cls.user = User.objects.create_user(**cls.credentials, is_superuser=True)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)
    def test_order_list_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Order")

    def test_order_list_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertRedirects(response, str(settings.LOGIN_URL))

class ProductsExportViewTestCase(TestCase):
    fixtures = [
        "products-fixture.json",
    ]

    def test_get_products_view(self):
        response = self.client.get(reverse("shopapp:products-export"))
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk" : product.pk,
                "name" : product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
        for product in products
        ]
        products_data = response.json
        self.assertEqual(
            products_data["products"],
            expected_data,
        )

class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='myusername', password='mypassword')
        cls.user = User.objects.create_user(**cls.credentials)
        cls.user.user_permissions.add(32)
        cls.user.save()
        cls.order = Order.objects.create(delivery_address="Panchenko 22", promocode="sale26", user=cls.user)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.order.delete()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)

    def test_order_details(self):
        response = self.client.get(
            reverse("shopapp:orders_detail", kwargs={"pk": self.order.pk})
        )

        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertTrue(Order.objects.filter(pk=self.order.pk).exists())

class OrdersExportViewTestCase(TestCase):
    fixtures = [
        "orders-fixture.json",
        "products-fixture.json",
        "users-fixture.json",
    ]

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='myusername', password='mypassword', is_staff=True)
        cls.user = User.objects.create_user(**cls.credentials)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)

    def test_get_orders_view(self):
        response = self.client.get(reverse("shopapp:orders-export"),)
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "pk" : order.pk,
                "delivery_address" : order.delivery_address,
                "promocode": order.promocode,
                "user": order.user_id,
                "products": [product.name for product in order.products.all()],
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data["orders"],
            expected_data,
        )