from django.shortcuts import render
from django.views import View
from .models import Tag, Author, Article, Category
from django.views.generic import ListView
class ArticleListView(ListView):
    queryset = (
        Article.objects.defer("content")
        .select_related("author")
        .prefetch_related("tags")
    )