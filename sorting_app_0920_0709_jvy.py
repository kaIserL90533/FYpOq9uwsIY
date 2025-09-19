# 代码生成时间: 2025-09-20 07:09:05
# sorting_app.py

"""
This Django application provides a set of sorting algorithms.

The app includes models, views, and URLs to demonstrate sorting functionality.
It follows Django best practices, includes docstrings, comments, and error handling.
"""

from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
import json

# Models
class SortableList(models.Model):
    """Model to store a list of integers."""
    values = models.TextField(help_text="Comma-separated list of integers.")

    def __str__(self):
        return f"SortableList: {self.values}"

# Views
class SortView(View):
    """
    View to perform sorting operations on a list of integers.
    Accepts a GET request with a list of integers to sort.
    Returns a JSON response with the sorted list.
    """
    def get(self, request, *args, **kwargs):
        try:
            # Retrieve the list of integers from the request
            list_str = request.GET.get('list', '')
            list_of_ints = [int(x) for x in list_str.split(',')]

            # Sort the list
            sorted_list = sorted(list_of_ints)

            # Return the sorted list in JSON format
            return JsonResponse({'sorted_list': sorted_list}, safe=False)
        except ValueError:
            # Handle non-integer values or conversion errors
            return JsonResponse({'error': 'Invalid input. Please provide a comma-separated list of integers.'}, status=400)

# URLs
urlpatterns = [
    path('sort/', SortView.as_view(), name='sort'),
]
