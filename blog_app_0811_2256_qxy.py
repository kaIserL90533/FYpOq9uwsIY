# 代码生成时间: 2025-08-11 22:56:56
from django.db import models
from django.urls import path
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View

# Data model for Blog
class Post(models.Model):
    """Represents a blog post."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# View for displaying all blog posts
class PostListView(View):
    """
    A simple view to display all blog posts.
    This view handles the GET method and returns a list of all blog posts.
    """
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        return render(request, 'blog/post_list.html', {'posts': posts})

# View for displaying a single blog post
class PostDetailView(View):
    """
    A view to display a single blog post.
    This view handles the GET method and returns the details of a single post.
    """
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})

# URL patterns for blog app
urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
