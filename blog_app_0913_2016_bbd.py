# 代码生成时间: 2025-09-13 20:16:02
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.views import View

"""
Blog application module for managing blog posts in a Django project.
"""

# Models
class BlogPost(models.Model):
    """A model representing a blog post."""
    title = models.CharField(max_length=200, help_text="The title of the blog post")
    content = models.TextField(help_text="The content of the blog post")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the post was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time when the post was last updated")
    
    def __str__(self):
        return self.title

# Views
class BlogListView(View):
    """A view to display a list of blog posts."""
    def get(self, request):
        try:
            posts = BlogPost.objects.all().order_by('-created_at')
            return render(request, 'blog_list.html', {'posts': posts})
        except Exception as e:
            # Log error and return an error response
            # Assuming logging is configured elsewhere in the project
            return HttpResponse("An error occurred while fetching blog posts.", status=500)

# URLs
urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blog-list'),
]
