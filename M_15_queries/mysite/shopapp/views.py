"""
В этом модуле лежат различные наборы представлений.

Разные view интеренет-магазина: по товарам, по заказам и т.д.
"""

from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import (HttpResponse, HttpRequest,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order, ImageProduct
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, OrderSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для скщностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = [
        "name",
        "description",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @extend_schema(
        summary= 'Get one product by id',
        description='Retrieves product, returns 404 if not found',
        responses={
            200 : ProductSerializer,
            404 : OpenApiResponse(description="Empty response, product by id not found"),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        OrderingFilter,
    ]
    filterset_fields = [
        "user",
        "delivery_address",
        "promocode",
        "products"
    ]
    ordering_fields = [
        "user",
        "products",
    ]

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "items": 1,
        }
        return render(request, 'shopapp/shop-index.html', context=context)

class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm,
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)

class ProductDetailView(DetailView):
    template_name = 'shopapp/products-detail.html'
    queryset = Product.objects.prefetch_related("images")
    context_object_name = 'products'


class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'

class ProductCreateView(PermissionRequiredMixin, CreateView):

    permission_required = "shopapp.add_product"
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    def test_func(self):
        return self.request.user == self.get_object().created_by or self.request.user.is_superuser

    permission_required = "shopapp.change_product"
    model = Product
    form_class = ProductForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:products_detail",
            kwargs={"pk" : self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ImageProduct.objects.create(
                products=self.object,
                image=image,
            )
        return response

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

class OrderListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('shopapp:orders_list')

class OrderUpdateView(UpdateView):
    model = Order
    fields = "user", "delivery_address", "promocode", "products",
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:orders_detail",
            kwargs={"pk" : self.object.pk},
        )

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')

class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products" : products_data})

class OrdersDataExportView(UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "pk" : order.pk,
                "delivery_address" : order.delivery_address,
                "promocode": order.promocode,
                "user": order.user_id,
                "products": [product.name for product in order.products.all()],
            }
            for order in orders
        ]
        return JsonResponse({"orders" : orders_data})