from django.contrib.auth.models import User
from django.core.management import BaseCommand
from typing import Sequence
from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo select fields")
        users_info = User.objects.values_list("username", flat = True)
        for u_info in users_info:
            print(u_info)
        #products_values = Product.objects.values("pk", "name")
        #for p_values in products_values:
        #    print(p_values)
        self.stdout.write("Done")
