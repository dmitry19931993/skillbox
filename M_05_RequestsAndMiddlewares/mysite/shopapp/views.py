from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from timeit import default_timer
from django.contrib.auth.models import Group
from  .models import Product, Order

def shop_index(request: HttpRequest):
    products = [
        ('Ноутбук', 2000),
        ('Компьютер', 2500),
        ('Смартфон', 1100),
    ]
    context = {
        'time_running': default_timer(),
        'products': products,
    }
    return render(request, 'shopapp/shop_index.html', context= context)

def groups_list(request: HttpRequest):
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups_list.html', context= context)

def products_list(request: HttpRequest):
    context = {
        'products' : Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context= context)

def orders_list(request: HttpRequest):
    context = {
        'orders' : Order.objects.select_related("user").prefetch_related('products').all(),
    }
    return render(request, 'shopapp/orders_list.html', context= context)