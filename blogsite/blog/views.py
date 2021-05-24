from django.shortcuts import render, get_object_or_404,get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from .forms import EmailPostForm, CommentForm, PostCreateForm,PostUpdateForm
from django.core.mail import send_mail
from django.db.models import Count
# Create your views here.

def post_list(request, tag_slug=None):
    """ Creates a view displaying a list of all posts. """

    object_list = Post.published.all().order_by("id")
    tag = None
   

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug) # get tag object given slug
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 2) # limits it to n posts per page
    page = request.GET.get('page') # current page number

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If the page is out of range deliver last page of the results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html', {'page':page, 'posts': posts, 'tag': tag})



def post_detail(request, year, month, day, post):
    """ Creates a view to show details of a single post. """
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    # posts_list = get_list_or_404(Post)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if  comment_form.is_valid():
            # create comment object but dont save to db
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
        
    return render(request, 'blog/post/detail.html', {'post': post,
                    'comments': comments,
                    'new_comments': new_comment,
                    'comment_form': comment_form,
                    'similar_posts': similar_posts
                    })


def post_share(request, post_id):
    """
    class describing email share
    """
    # retrieve the post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method =='POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
            # send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
 
#  def post_edit(request, post_id)
# def post_edit(request, post):
#     """
#     create or edit posts
#     """
#     post = get_object_or_404(Post,pk=pk)
#     if request.method == 'POST':
#         post_form = PostForm(
#             instance=request.POST)
#         if post_form.is_valid():
#             post_form.save()
#     else:
#         post_form = PostForm()
#     return render(request,'blog/post/edit.html', {'post_form': post_form})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post/post-create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        """if form is valid save the model as"""
        post = form.save(commit=False)
        post.author = self.request.user.get_username()

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'blog/post/post_update.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'
    

    def form_valid(self, form):
        """
        extra fields are generated
        """
        post = form.save(commit=False)
        post.updated_by = self.request.user.get_username() # set user who updated form
        post.save()
        return super().form_valid(form)

