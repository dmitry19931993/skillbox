from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from timeit import default_timer

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