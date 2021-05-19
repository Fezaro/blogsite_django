from django import forms
from .models import Comment, Post


class EmailPostForm(forms.Form):
    """
    class to deal with emails
    """
    name =  forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        widget=forms.Textarea,
        required=False)

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('name','email','body')


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'status', 'tags', 'body', 'publish')

class PostUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'tags', 'body', 'status')
