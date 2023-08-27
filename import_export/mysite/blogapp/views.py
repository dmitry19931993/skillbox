from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.views import View
from .models import Tag, Author, Article, Category
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy
class ArticleListView(ListView):
    queryset = (
        Article.objects.defer("content")
        .select_related("author")
        .prefetch_related("tags")
    )

class ArticleDetailView(DetailView):
    model = Article

class LatestArticlesFeed(Feed):
    title = "Blog article (latest)"
    description = "Upadates on changes and addition blog articles"
    link = reverse_lazy("blogapp:articles_list")

    def items(self):
        return (
            Article.objects.order_by("-pub_date")[:5]
        )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]