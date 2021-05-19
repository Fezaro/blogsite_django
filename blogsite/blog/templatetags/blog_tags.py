from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
from account.models import Profile
import markdown

# creating simple tag to retrieve total posts

register = template.Library()

@register.simple_tag
# Django uses the functions name as the tag name.
# specify a 'name' attribute to have a custom name for the tag
#  @register.simple_tag(name='my_tag') 

def total_posts():
    """
    returns total posts published
    """
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
# returns a rendered template
# has to return a dictionary of values
# allows us to specify an optional no. of posts through the tag
def show_latest_posts(count=3):
    """
    returns latest posts published
    """
    profile = Profile.photo
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts, 'photo': profile }

@register.simple_tag
def get_most_commented_posts(count=5):
    """
    returns upto 5 most commented posts published
    """
    return Post.published.annotate(
        total_comments=Count('comments')
        ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    """
    return markdown converted text
    """
    return mark_safe(markdown.markdown(text, extensions=['pymdownx.emoji']))
