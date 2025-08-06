# 代码生成时间: 2025-08-06 23:07:05
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import ExampleModel
from .serializers import ExampleSerializer
import logging

"""
This module provides a utility class to format responses from Django REST Framework views.
It uses DRF serializers to ensure that the response is in the correct format.
"""


class ApiResponseFormatter:
    """
    A utility class to format API responses consistently.
    """

    def format_response(self, data, status_code=status.HTTP_200_OK, extra_context=None):
        """
        Formats the response data using the ApiResponseFormatter.
        
        :param data: The data to be formatted in the response.
        :param status_code: The HTTP status code for the response.
        :param extra_context: Extra context to include in the response.
        :return: A JSON response with the formatted data.
        """
        context = {'data': data}
        if extra_context:
            context.update(extra_context)
        return Response(context, status=status_code)


class ExampleModelAPIView(APIView):
    """
    An example view demonstrating the use of ApiResponseFormatter.
    """
    response_formatter = ApiResponseFormatter()

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests.
        """
        try:
            example_model_instance = ExampleModel.objects.get(id=1)
            serializer = ExampleSerializer(example_model_instance)
            return self.response_formatter.format_response(serializer.data)
        except ExampleModel.DoesNotExist:
            return self.response_formatter.format_response(
                {'error': 'ExampleModel instance not found'},
                status_code=status.HTTP_404_NOT_FOUND,
                extra_context={'message': 'The requested resource was not found.'}
            )

    # You can add more methods (e.g., post, put, delete) as needed.

# Example usage of the ApiResponseFormatter in a URL configuration:
# from django.urls import path
# from .views import ExampleModelAPIView

# urlpatterns = [
#     path('example-model/', ExampleModelAPIView.as_view(), name='example-model-api'),
# ]
