from django.contrib.auth.models import User
from django.core.management import BaseCommand
from typing import Sequence
from django.db import transaction
from shopapp.models import Order, Product


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create order with products")
        user = User.objects.get(username="admin")
        #products: Sequence[Product] = Product.objects.defer(
        #    "descrption",
        #    "price",
        #    "created_at"
        #).all() #С базы данных запрашиваются все поля кроме указанных

        products: Sequence[Product] = Product.objects.only("id").all() #С базы данных запрашиваются только указанные поля

        order, created = Order.objects.get_or_create(
            delivery_address="ul Panchenko, d 8",
            promocode="promo1",
            user=user,
        )
        for product in products:
            order.products.add(product)
        self.stdout.write(f"Created order {order}")
