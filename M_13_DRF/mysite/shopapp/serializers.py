from rest_framework import serializers
from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "description",
            "discount",
            "price",
            "created_at",
            "archived",
            "preview",
        )

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "pk",
            "user",
            "delivery_address",
            "promocode",
            "products",
            "created_at",
            "receipt",
        )