from .models import Product, Order
from django.contrib.auth.models import Group
from django.forms import ModelForm

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount"


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "user", "delivery_address", "promocode", "products"

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ("name",)