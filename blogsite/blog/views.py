from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def post_list(request):
    """ Creates a view displaying a list of all posts. """
    
    current_page = 1
    object_list = Post.published.all().order_by("id")
    paginator = Paginator(object_list, 1) # limits it to n posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If the page is out of range deliver last page of the results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html', {'page':page, 'posts': posts})



def post_detail(request, year, month, day, post):
    """ Creates a view to show details of a single post. """
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    
    return render(request, 'blog/post/detail.html', {'post':post})

