from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpRequest


def login_view(request: HttpRequest):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, pasword=password)

    if user is not None:
        login(request, user)
        return redirect('/admin/')

    return render(request, 'myauth/login.html', {'error' : 'Invalid login credentials'})


