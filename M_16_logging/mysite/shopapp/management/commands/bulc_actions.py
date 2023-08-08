from django.contrib.auth.models import User
from django.core.management import BaseCommand
from typing import Sequence
from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")
        result = Product.objects.filter(
            name__contains= "smartphone",
        ).update(discount=10)               #Массово обновляет указанные строки в таблице

        print(result)

        #info = [
        #    ("smartphone_12", 1234),
        #    ("smartphone_13", 134),
        #    ("smartphone_14", 12344),
        #]
        #products = [
        #    Product(name=name, price=price, created_by_id = 1)
        #    for name, price, in info
        #]
        #result = Product.objects.bulk_create(products) #Заполняются только указанные поля
        #for obj in result:
        #    print(obj)
        self.stdout.write("Done")
