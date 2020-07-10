from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    #post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
]

# < > are used to capture values from the url . path converters are used to define the url patterns 
