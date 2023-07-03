from django.urls import path

from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailView,
    ProductListView,
    OrderDetailView,
    OrderListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderCreateView,
)

app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="products_detail"),
    path("products/<int:pk>/update", ProductUpdateView.as_view(), name="products_update"),
    path("products/<int:pk>/archive", ProductDeleteView.as_view(), name="products_archive"),
    path("products/create", ProductCreateView.as_view(), name="create-product"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("orders/create", OrderCreateView.as_view(), name="create-order"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="orders_detail"),
]
