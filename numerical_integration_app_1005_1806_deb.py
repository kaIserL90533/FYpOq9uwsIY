# 代码生成时间: 2025-10-05 18:06:53
from django.apps import AppConfig
from django.urls import path
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import numpy as np

"""
A Django application for numerical integration calculation.
"""
class NumericalIntegrationAppConfig(AppConfig):
    name = 'numerical_integration_app'
    verbose_name = 'Numerical Integration Calculator'

"""
Model to store integration problems.
"""
from django.db import models

class IntegrationProblem(models.Model):
    # Fields for the integration problem
    function = models.CharField(max_length=255)
    lower_limit = models.FloatField()
    upper_limit = models.FloatField()
    # Add more fields as needed

    def __str__(self):
        return f"Integrate {self.function} from {self.lower_limit} to {self.upper_limit}"

"""
View to handle the numerical integration calculation.
"""
@csrf_exempt
def integrate(request):
    """
    Perform numerical integration based on the input function and limits.
    Returns a JSON response with the result.
    """
    if request.method == 'POST':
        data = request.POST
        try:
            function = data.get('function')
            lower_limit = float(data.get('lower_limit'))
            upper_limit = float(data.get('upper_limit'))
            
            # Validate inputs
            if lower_limit >= upper_limit:
                response = {'error': 'Lower limit must be less than upper limit.'}
            else:
                # Perform integration using numpy's quad function
                result, error, _ = quad(lambda x: eval(function), lower_limit, upper_limit)
                response = {'result': result}
        except Exception as e:
            response = {'error': str(e)}
    else:
        response = {'error': 'Invalid request method.'}
    return JsonResponse(response)

"""
URL configuration for the numerical integration view.
"""
urlpatterns = [
    path('integrate/', integrate, name='integrate'),
]
