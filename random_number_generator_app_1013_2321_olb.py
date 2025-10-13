# 代码生成时间: 2025-10-13 23:21:47
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
import random
"""
Django application for generating random numbers.
"""

class RandomNumberGeneratorModel(models.Model):
    """
    A simple model to store generated random numbers.
    """
    number = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.number)

class RandomNumberGeneratorView(View):
    """
    View to generate and return a random number within a specified range.
    """
    def get(self, request, *args, **kwargs):
        try:
            # Assuming the range is given as query parameters 'min' and 'max'
            min_val = request.GET.get('min', 0)
            max_val = request.GET.get('max', 100)
            
            # Validate the input parameters
            min_val = int(min_val)
            max_val = int(max_val)
            
            if min_val > max_val:
                return JsonResponse({'error': 'Minimum value cannot be greater than maximum value.'}, status=400)
            
            # Generate a random number
            random_number = random.randint(min_val, max_val)
            return JsonResponse({'random_number': random_number})
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid range values provided.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def get_random_number_urls():
    """
    Returns the URL patterns for the random number generator.
    """
    return [
        path('random/', RandomNumberGeneratorView.as_view(), name='random_number_generator'),
    ]
