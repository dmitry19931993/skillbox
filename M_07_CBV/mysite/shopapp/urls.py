from django.urls import path

from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailView,
    ProductListView,
    orders_list,
    create_product,
    create_order
)

app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="products_detail"),
    path("products/create", create_product, name="create-product"),
    path("orders/", orders_list, name="orders_list"),
    path("orders/create", create_order, name="create-order")
]
