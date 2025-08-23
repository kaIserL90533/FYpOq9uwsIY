# 代码生成时间: 2025-08-23 10:56:46
from django.conf.urls import url
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ImproperlyConfigured
import random

def generate_random_number(min_val=0, max_val=100):
    """
    Generate a random number between min_val and max_val.

    Args:
        min_val (int): The minimum value of the random number.
        max_val (int): The maximum value of the random number.

    Returns:
        int: A random integer between min_val and max_val.
    """
    return random.randint(min_val, max_val)

def generate_random_number_view(request):
    """
    API view to generate a random number.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        JsonResponse: A JSON response with the random number.
    """
    try:
        query_min = request.GET.get('min', 0)
        query_max = request.GET.get('max', 100)
        min_val = int(query_min)
        max_val = int(query_max)
        random_number = generate_random_number(min_val, max_val)
        return JsonResponse({'random_number': random_number})
    except ValueError as e:
        return JsonResponse({'error': 'Invalid input.'}, status=400)

def random_number_urls():
    """
    Define the URL patterns for the random number generator app.

    Returns:
        list: A list of URL patterns.
    """
    return [
        url(r'^random_number/$', generate_random_number_view, name='random_number'),
    ]
