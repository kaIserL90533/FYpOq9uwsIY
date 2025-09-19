# 代码生成时间: 2025-09-19 20:13:41
# Django application for managing configuration files

# models.py
"""
Models for the Configuration Manager application.
"""
from django.db import models

class Configuration(models.Model):
    """Model to store configuration data."""
    key = models.CharField(max_length=255, unique=True, help_text="Configuration key")
    value = models.TextField(help_text="Configuration value")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the configuration")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key}: {self.value}"

# views.py
"""
Views for the Configuration Manager application.
"""
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Configuration

@method_decorator(csrf_exempt, name='dispatch')
class ConfigurationView(View):
    """
    A view to handle CRUD operations for Configuration data.
    """
    def get(self, request, *args, **kwargs):
        """
        Retrieve the configuration.
        """
        configurations = Configuration.objects.all()
        return JsonResponse(list(configurations.values()), safe=False)

    def post(self, request, *args, **kwargs):
        """
        Create a new configuration.
        """
        key = request.POST.get('key')
        value = request.POST.get('value')
        description = request.POST.get('description', '')
        try:
            Configuration.objects.create(key=key, value=value, description=description)
            return JsonResponse({'status': 'success'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        """
        Update an existing configuration.
        """
        key = request.POST.get('key')
        value = request.POST.get('value')
        description = request.POST.get('description', '')
        try:
            config, created = Configuration.objects.get_or_create(key=key)
            config.value = value
            config.description = description
            config.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        """
        Delete a configuration.
        """
        key = request.POST.get('key')
        try:
            Configuration.objects.get(key=key).delete()
            return JsonResponse({'status': 'success'}, status=204)
        except Configuration.DoesNotExist:
            return JsonResponse({'error': 'Configuration not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# urls.py
"""
URLs for the Configuration Manager application.
"""
from django.urls import path
from .views import ConfigurationView

urlpatterns = [
    path('configuration/', ConfigurationView.as_view(), name='configuration'),
]
