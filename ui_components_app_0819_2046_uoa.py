# 代码生成时间: 2025-08-19 20:46:15
# Django application for a UI Components Library
"""
This Django application provides a library of user interface components
for use in web applications. It follows Django's best practices, includes
models, views, and URLs, and has docstrings and comments for clarity. It
also handles errors properly.
"""

# Import necessary Django components
from django.apps import AppConfig
from django.conf.urls import url
from django.http import JsonResponse
from django.views import View
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class UIComponent(models.Model):
    """Model representing a UI component."""
    name = models.CharField(max_length=255, help_text="The name of the component.")
    html_template = models.TextField(help_text="The HTML template of the component.")

    def __str__(self):
        return self.name



class ComponentListView(View):
    """View for listing all UI components."""
    def get(self, request, *args, **kwargs):
        try:
            components = UIComponent.objects.all()
            component_list = [component.html_template for component in components]
            return JsonResponse({'components': component_list}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class ComponentDetailView(View):
    """View for retrieving a single UI component by name."""
    def get(self, request, name, *args, **kwargs):
        try:
            component = UIComponent.objects.get(name=name)
            return JsonResponse({'html_template': component.html_template})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Component not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class UIComponentsAppConfig(AppConfig):
    """Configuration for the UI Components application."""
    name = 'ui_components'
    verbose_name = 'UI Components'

    def ready(self):
        # This function is called when the application is loaded.
        pass


# URL patterns for the UI Components application
urlpatterns = [
    url(r'^list/$', ComponentListView.as_view(), name='component_list'),
    url(r'^(?P<name>[\w-]+)/$', ComponentDetailView.as_view(), name='component_detail'),
]
