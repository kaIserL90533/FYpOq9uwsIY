# 代码生成时间: 2025-08-31 21:29:52
# blog_app/models.py
"""
Models definitions for the Blog application.
"""
from django.db import models

class Post(models.Model):
    """
    Represents a blog post.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    def __str__(self):
        """Return a string representation of the Post."""
        return self.title

# blog_app/views.py
"""
Views for the Blog application.
"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Post

def post_list(request):
    """Display a list of all posts."""
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    """Display a detail page for a single post."""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, 'blog/post_detail.html', {'post': post})

# blog_app/urls.py
"""
URL patterns for the Blog application.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]

# blog_app/admin.py
"""
Django admin interface for the Blog application.
"""
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'author')
    search_fields = ('title',)
    list_filter = ('date_posted',)

# blog_app/apps.py
"""
Configuration for the Blog application.
"""
from django.apps import AppConfig

class BlogConfig(AppConfig):
    name = 'blog_app'
    verbose_name = 'Blog'

# blog_app/tests.py
"""
Unit tests for the Blog application.
"""
from django.test import TestCase
from .models import Post

class PostModelTest(TestCase):
    def test_str(self):
        """Test the string representation of the Post model."""
        post = Post.objects.create(title='Test post')
        self.assertEqual(str(post), post.title)

# blog_app/forms.py
"""
Forms for the Blog application.
"""
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """
    A form for creating and updating blog posts.
    """
    class Meta:
        model = Post
        fields = ('title', 'content',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'post-title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'id': 'post-content'}),
        }

# blog_app/templates/blog/post_list.html
"""
Template for displaying a list of blog posts.
"""
{% for post in posts %}
    <div class="post">
        <h2>{{ post.title }}</h2>
        <p>{{ post.date_posted }}</p>
        <p>{{ post.content }}</p>
    </div>
{% endfor %}

# blog_app/templates/blog/post_detail.html
"""
Template for displaying a single blog post.
"""
<h1>{{ post.title }}</h1>
<p>{{ post.date_posted }}</p>
<p>{{ post.content }}</p>