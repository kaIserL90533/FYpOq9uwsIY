# 代码生成时间: 2025-09-22 10:09:29
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import math
import json

"""
Math Tools App
This Django app provides a collection of mathematical calculation tools.
"""

class MathToolView(View):
    """
    A Django view class providing an API endpoint for mathematical calculations.
    """

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        """
        Allowing CSRF exemption for this API endpoint.
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        GET endpoint not supported.
        """
        return JsonResponse({'error': 'GET method not supported'}, status=405)

    def post(self, request):
        """
        POST endpoint to perform mathematical calculations.
        """
        try:
            data = json.loads(request.body)
            operation = data.get('operation')
            num1 = data.get('num1')
            num2 = data.get('num2')

            # Perform calculation based on the operation
            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 != 0:
                    result = num1 / num2
                else:
                    raise ValueError('Cannot divide by zero.')
            elif operation == 'power':
                result = math.pow(num1, num2)
            else:
                raise ValueError('Unsupported operation.')

            return JsonResponse({'result': result})
        except (ValueError, TypeError, ObjectDoesNotExist) as e:
            return JsonResponse({'error': str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    def put(self, request):
        """
        PUT endpoint not supported.
        """
        return JsonResponse({'error': 'PUT method not supported'}, status=405)

    def delete(self, request):
        """
        DELETE endpoint not supported.
        """
        return JsonResponse({'error': 'DELETE method not supported'}, status=405)

# URL configuration
# This should be added to the project's urls.py
# from django.urls import path
# from .views import MathToolView
# urlpatterns = [
#     path('math/', MathToolView.as_view(), name='math_tool'),
# ]