from django.contrib.sitemaps import Sitemap

from pizzami.foods.models import Food


class FoodSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Food.objects.confirmed()

    def lastmod(self, obj):
        return obj.updated_at
