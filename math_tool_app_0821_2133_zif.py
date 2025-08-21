# 代码生成时间: 2025-08-21 21:33:11
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
import json
import math

defs = {
    "add": "Performs addition of two numbers",
    "subtract": "Performs subtraction of two numbers",
    "multiply": "Performs multiplication of two numbers",
    "divide": "Performs division of two numbers"
}

def calculate(func, num1, num2):
    """Perform mathematical calculation based on the function name."""
    try:
        if func == "add":
            return num1 + num2
        elif func == "subtract":
            return num1 - num2
        elif func == "multiply":
            return num1 * num2
        elif func == "divide":
            if num2 == 0:
                raise ValueError("Cannot divide by zero.")
            return num1 / num2
        else:
            raise ValueError("Invalid function name.")
    except Exception as e:
        return str(e)


def math_info(request, func):
    """View function to return information about a mathematical function."""
    try:
        info = defs.get(func, "Function not found.")
        return JsonResponse({'info': info})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def math_calculate(request):
    """View function to perform mathematical calculations based on request data."""
    try:
        request_data = json.loads(request.body)
        func = request_data['function']
        num1 = float(request_data['number1'])
        num2 = float(request_data['number2'])
        result = calculate(func, num1, num2)
        return JsonResponse({'result': result})
    except ValueError as ve:
        return JsonResponse({'error': str(ve)})
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred.'})

# URLs for the math_tool_app
urlpatterns = [
    path("math/info/<str:func>/", math_info, name="math_info"),
    path("math/calculate/", math_calculate, name="math_calculate"),
]
