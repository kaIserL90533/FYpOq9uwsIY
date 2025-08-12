# 代码生成时间: 2025-08-12 09:06:19
from django.urls import path
from django.http import JsonResponse
from django.views import View
from django.db import models
import random

def generate_random_number(min_value, max_value):
    """
    Generates a random number between min_value and max_value.

    Args:
        min_value (int): The minimum possible value.
        max_value (int): The maximum possible value.

    Returns:
        int: A random number within the specified range.
    """
    return random.randint(min_value, max_value)

class RandomNumberGenerator(models.Model):
    """
    Model to represent a random number generator entry.

    Attributes:
        number (int): The generated random number.
    """
    number = models.IntegerField()

    def __str__(self):
        return f"RandomNumberGenerator({self.number})"

class RandomNumberView(View):
    """
    View to handle requests for generating random numbers.

    GET Parameters:
        min_value (int): Optional minimum value for the random number.
        max_value (int): Optional maximum value for the random number.
    """
    def get(self, request):
        min_value = request.GET.get('min_value', 1)
        max_value = request.GET.get('max_value', 100)
        try:
            min_value = int(min_value)
            max_value = int(max_value)
            if min_value >= max_value:
                return JsonResponse({'error': 'min_value must be less than max_value'}, status=400)
            random_number = generate_random_number(min_value, max_value)
            RandomNumberGenerator.objects.create(number=random_number)
            return JsonResponse({'random_number': random_number})
        except ValueError:
            return JsonResponse({'error': 'min_value and max_value must be integers'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

app_name = 'random_number_generator'
urlpatterns = [
    path('generate/', RandomNumberView.as_view(), name='generate'),
]
