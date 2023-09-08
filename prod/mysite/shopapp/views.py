"""
В этом модуле лежат различные наборы представлений.

Разные view интеренет-магазина: по товарам, по заказам и т.д.
"""

import logging
from timeit import default_timer
from csv import DictWriter

from django.contrib.syndication.views import Feed
from django.contrib.auth.models import Group
from django.http import (HttpResponse, HttpRequest,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import render, redirect, reverse
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order, ImageProduct
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, OrderSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .common import save_csv_products
from django.shortcuts import render, get_object_or_404



log = logging.getLogger(__name__)


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

    @action(methods=['get'], detail=False)
    def download_scv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "price",
            "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames= fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response

    @action(
        methods= ['post'],
        detail= False,
        parser_classes= [MultiPartParser],
    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60*2))
    def list(self, *args, **kwargs):
        print("Hello products list")
        return super().list(*args, **kwargs)
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
        log.debug("Products for shop index: %s", products)
        log.info("Rendering shop index")
        print('shop index contest', context)
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

class LatestProductsFeed(Feed):
    title = "Products (latest)"
    description = "Upadates on changes and addition products"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return (
            Product.objects.order_by("-created_at")[:5]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]


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
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
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
            cache.set(cache_key, products_data, 300)
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

class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/user-order-list.html'
    def get_queryset(self):
        self.owner = get_object_or_404(User, pk= self.kwargs['user_id'])
        queryset = Order.objects.filter(user_id= self.owner)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context

class UserOrdersDataExportView(View):


    def get(self, request: HttpRequest, user_id= "user_id") -> JsonResponse:
        cache_key = "orders_data_export"
        orders_data = cache.get(cache_key)
        if orders_data is None:
            self.owner = get_object_or_404(User, pk=self.kwargs['user_id'])
            orders = Order.objects.order_by("pk").filter(user_id=self.owner)
            orders_data = [
                {
                    "pk": order.pk,
                    "delivery_address": order.delivery_address,
                    "promocode": order.promocode,
                    "products": [product.name for product in order.products.all()],
                }
                for order in orders
            ]
            cache.set(cache_key, orders_data, 300)

        return JsonResponse({f"orders by {self.owner}": orders_data})