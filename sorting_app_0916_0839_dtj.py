# 代码生成时间: 2025-09-16 08:39:30
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
import json

# 排序算法实现
class SortingAlgorithmView(View):
    """
    View to handle sorting algorithm requests.
    """
    def get(self, request):
        """
        Handles GET requests to retrieve the sorting algorithm page.
        """
        return JsonResponse({'message': 'Sorting Algorithm Page'})
    
    def post(self, request):
        """
        Handles POST requests to sort a list of numbers.
        """
        try:
            data = json.loads(request.body)
            if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
                raise ValueError('Data must be a list of numbers.')
            # Bubble sort algorithm
            sorted_data = self.bubble_sort(data)
            return JsonResponse({'sorted_data': sorted_data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    def bubble_sort(self, data):
        """
        Implements the bubble sort algorithm.
        """
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data


# Define the URL patterns
urlpatterns = [
    path('sort/', SortingAlgorithmView.as_view(), name='sorting_algorithm'),
]
