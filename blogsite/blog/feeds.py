from  django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostsFeed(Feed):
    """
    docstrinreal Simple Syndication feed of latest posts
    """
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    def items(self):
        """items to include in RSS feed"""
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        
        return truncatewords(item.body, 30)