from django.core.urlresolvers import reverse
from django.contrib import sitemaps

from blog import models as blog_models


class StaticPagesSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'about', ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(sitemaps.Sitemap):
    changefreq = "hourly"
    priority = 0.8

    def items(self):
        return blog_models.Post.objects.filter(status=blog_models.ITEM_STATUS_PUBLISHED)

    def lastmod(self, obj):
        return obj.modified_at


sitemaps_dict = {
    'static': StaticPagesSitemap,
    'blog': BlogSitemap
}

