# 代码生成时间: 2025-08-02 09:55:53
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views import View
import json
import os

"""
A Django application component to manage configuration files.
This component includes models, views, and URLs as needed.
"""

# Models
class Config(models.Model):
    """Model to represent a configuration file."""
    file_name = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name

# Views
class ConfigListView(View):
    """View to list all configuration files."""
    def get(self, request):
        configs = Config.objects.all()
        return JsonResponse(list(configs.values('file_name', 'created_at', 'updated_at')), safe=False)

class ConfigDetailView(View):
    """View to retrieve, update, or delete a specific configuration file."""
    def get(self, request, file_name):
        config = get_object_or_404(Config, file_name=file_name)
        return JsonResponse(config.to_dict())
    
    def put(self, request, file_name):
        config = get_object_or_404(Config, file_name=file_name)
        content = request.POST.get('content')
        if content:
            config.content = content
            config.save()
            return JsonResponse(config.to_dict())
        else:
            return HttpResponse(status=400)
    
    def delete(self, request, file_name):
        config = get_object_or_404(Config, file_name=file_name)
        config.delete()
        return HttpResponse(status=204)

# URLs

urlpatterns = [
    # List all configuration files
    path('configs/', ConfigListView.as_view(), name='config-list'),
    # Retrieve, update, or delete a specific configuration file
    path('configs/<str:file_name>/', ConfigDetailView.as_view(), name='config-detail'),
]

# Helper function to convert model instance to dictionary representation
def to_dict(self):
    return {
        'file_name': self.file_name,
        'content': self.content,
        'created_at': self.created_at.isoformat(),
        'updated_at': self.updated_at.isoformat()
    }

# Add the 'to_dict' method to the Config model
Config.to_dict = to_dict

# Error handling
# In a real-world scenario, you would handle errors more gracefully,
# possibly by using Django's built-in exception handling and middleware.
# Here's a simple example of how you might handle errors:

@login_required
@require_http_methods(['GET', 'PUT', 'DELETE'])
def error_handling_decorator(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Config.DoesNotExist:
            return JsonResponse({'error': 'Configuration file not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return _wrapped_view

# You would then decorate your views with this decorator:
# @error_handling_decorator
# class ConfigDetailView(View):
#     ...
