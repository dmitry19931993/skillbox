from django.contrib.auth.models import Group
from shopapp.models import Product, Order
from rest_framework import serializers

class GroupSelializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "pk", "name",

class ProductSelializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "pk", "name",

class OrderSelializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "pk", "user", "products"