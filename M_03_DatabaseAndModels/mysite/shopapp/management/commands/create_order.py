from django.core.management import BaseCommand
from shopapp.models import Order
from django.contrib.auth.models import User
class Command(BaseCommand):
    """
    Create orders
    """

    def handle(self, *args, **options):
        self.stdout.write('Create order')
        user = User.objects.get(username='admin')
        order = Order.objects.get_or_create(
            delivery_address = "ul P-Panchenko, d 22",
            promocode = "SALE234",
            user = user,
        )
        self.stdout.write(f'Create order {order}')