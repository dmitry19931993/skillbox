from django.urls import path, include
from rest_framework.routers import DefaultRouter

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
    OrdersDataExportView,
    OrderUpdateView,
    OrderDeleteView,
    ProductsDataExportView,
    ProductViewSet,
    OrderViewSet,
)

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)



app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/export/", ProductsDataExportView.as_view(), name="products-export"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="products_detail"),
    path("products/<int:pk>/update", ProductUpdateView.as_view(), name="products_update"),
    path("products/<int:pk>/archive", ProductDeleteView.as_view(), name="products_archive"),
    path("products/create", ProductCreateView.as_view(), name="create-product"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("orders/export/", OrdersDataExportView.as_view(), name="orders-export"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="orders_detail"),
    path("orders/<int:pk>/update", OrderUpdateView.as_view(), name="orders_update"),
    path("orders/<int:pk>/delete", OrderDeleteView.as_view(), name="orders_delete"),
    path("orders/create", OrderCreateView.as_view(), name="create-order"),

]
