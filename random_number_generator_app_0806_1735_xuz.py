# 代码生成时间: 2025-08-06 17:35:33
# random_number_generator_app/models.py
from django.db import models

"""
Model representing a Random Number Generator entry.
"""
class RandomNumber(models.Model):
    number = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.number)

# random_number_generator_app/views.py
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError
from .models import RandomNumber
import random

"""
View to generate and return a random number.
"""
class RandomNumberGenerator(View):
    def get(self, request):
        try:
            number = random.randint(1, 100)
            RandomNumber.objects.get(number=number)
            # If the number is already taken, generate another one.
            return self.get(request)
        except RandomNumber.DoesNotExist:
            new_number = RandomNumber(number=number)
            new_number.save()
            return JsonResponse({'number': number})

# random_number_generator_app/urls.py
from django.urls import path
from .views import RandomNumberGenerator

"""
URL configuration for the Random Number Generator app.
"""
urlpatterns = [
    path('random-number/', RandomNumberGenerator.as_view(), name='random_number_generator'),
]

# random_number_generator_app/tests.py
from django.test import TestCase
from .models import RandomNumber
import random

"""
Test cases for the Random Number Generator app.
"""
class RandomNumberGeneratorTestCase(TestCase):
    def test_random_number_generation(self):
        generated_number = RandomNumber.objects.create(number=random.randint(1, 100))
        self.assertTrue(1 <= generated_number.number <= 100)

    def test_unique_number(self):
        number = random.randint(1, 100)
        RandomNumber.objects.create(number=number)
        with self.assertRaises(ValidationError):
            RandomNumber.objects.create(number=number)

    def test_number_retrieval(self):
        generated_number = RandomNumber.objects.create(number=random.randint(1, 100))
        response = self.client.get('/random-number/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('number', response.json())