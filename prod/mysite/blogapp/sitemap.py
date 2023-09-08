from django.contrib.sitemaps import Sitemap

from .models import Article

class BlogSitemap(Sitemap):
    changefriq = "never"
    priority = 0.5
    def items(self):
        return (
            Article.objects.all()
        )

    def lastmod(self, obj: Article):
        return obj.pub_date