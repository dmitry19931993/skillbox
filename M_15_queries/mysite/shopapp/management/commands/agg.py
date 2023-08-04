from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db.models import Avg, Max, Min, Count, Sum
from typing import Sequence
from shopapp.models import Product, Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo agregate")
        #result = Product.objects.aggregate(
        #    Avg("price"),
        #    Max("price"),
        #    Min("price"),
        #    Count("id"),
        #)
        #print(result)

        orders = Order.objects.annotate(
            total=Sum("products__price", default=0),
            products_count=Count("products"),
        )
        for order in orders:
            print(
                f"Order # {order.id}"
                f"with {order.products_count}"
                f"product worth {order.total}"
            )
        self.stdout.write("Done")
