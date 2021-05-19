from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    """
    creating a sitemap for the site
    """
    # The changefreq and priority attributes indicate the
    # change frequency of your post pages and their relevance in your
    # website (the maximum value is 1)
    changefreq = 'weekly'
    priority =  0.9

    # specify url for each object by adding 'location' method

    def items(self):
        """
        returns all posts published
        """
        return Post.published.all()
    def lastmod(self, obj):
        """returns last time object from items was modified"""
        return obj.updated