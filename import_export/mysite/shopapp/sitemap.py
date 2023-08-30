from django.contrib.sitemaps import Sitemap

from .models import Product

class ShopSitemap(Sitemap):
    changefriq = "always"
    priority = 0.5
    def items(self):
        return (
            Product.objects.filter(name__contains="Phone")
        )
    def lastmod(self, obj: Product):
        return obj.created_at