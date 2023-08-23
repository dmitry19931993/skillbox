from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (
    get_cookie_view,
    set_cookie_view,
    get_session_view,
    set_session_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    FooBarView,
    UserUpdateView,
    UserListView,
    UserDetailView,
    HelloWorldView,)

app_name = "myauth"

urlpatterns = [
    path("login/",
         LoginView.as_view(
             template_name="myauth/login.html",
             redirect_authenticated_user=True,
         ),
         name="login"),
    path("hello/", HelloWorldView.as_view(), name="hello"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("users/", UserListView.as_view(), name="users"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="users_detail"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("about-me/<int:pk>/update/", UserUpdateView.as_view(), name="update"),
    path("register/", RegisterView.as_view(), name="register"),
    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path('cookie/set/', set_cookie_view, name="cookie-set"),
    path("session/get/", get_session_view, name="session-get"),
    path('session/set/', set_session_view, name="session-set"),
    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
]
