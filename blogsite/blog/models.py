from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

# Adding a model manager, there aare two ways:
#  1. Add extra manager methods ( Post.objects.my_manager() )
#  2. Modify initial manager querysets  ( Post.my_manager.all() )
# create the class using manager querysets

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):
    """model describing posts on the blog"""
    objects = models.Manager() # The default manager
    published = PublishedManager() # our custom manager
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish') # unique_for_date ensures only one post with a given slug date for multiple posts on the same day
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True,on_delete=models.CASCADE, related_name='+')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()
    class meta:
        ordering = ('-publish',)

    def __str__(self):
        """string representation of model object"""
        return self.title

    def get_absolute_url(self):
        """returns the url to accesss a detail record for this post"""
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    
class Comment(models.Model):
    """
    model representing comments on blog
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # attribute allows us to name the attribute that we use for the relation from the
    #  related object back to this one.
    # Django will use the name of the model in lowercase, followed by _set to name the
    # manager of the related object
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) # for manually deactivating inappropriate comments,

    class Meta:
        ordering =('created',)
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}.'

