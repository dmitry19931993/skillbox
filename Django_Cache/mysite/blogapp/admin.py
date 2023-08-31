from django.contrib import admin

from .models import Article, Author, Tag, Category

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "bio"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "name"

@admin.register(Tag)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "name"

@admin.register(Article)
class CategoryAdmin(admin.ModelAdmin):

    list_display = "pk", "title", "content", "pub_date", "author", "category"