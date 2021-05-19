from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    #post views
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('', views.tag_list, name="tag_cloud"), 
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
]

# < > are used to capture values from the url . path converters are used to define the url patterns 
