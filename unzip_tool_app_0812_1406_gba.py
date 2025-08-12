# 代码生成时间: 2025-08-12 14:06:57
# unzip_tool_app/__init__.py
def __init__(self):
    pass


# unzip_tool_app/models.py"""
Defines the models for the Unzip Tool application.
"""
def __init__(self):
    pass


# unzip_tool_app/views.py"""
Handles the views for the Unzip Tool application.
"""
def __init__(self):
    pass

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage
from zipfile import ZipFile
import os


# File system path for uploaded files
FILE_SYSTEM_PATH = 'uploads/'

@require_http_methods(['POST'])
def unzip_file(request):
    """
    Unzips a file uploaded by the user.
    Receives a zip file in a POST request, extracts its contents, and returns a success message.
    
    :param request: Django HTTP request object.
    :return: JSON response indicating success or failure.
    """
    try:
        # Check if the request contains a zip file
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file was uploaded.'}, status=400)

        uploaded_file = request.FILES['file']
        if not uploaded_file.name.endswith('.zip'):
            return JsonResponse({'error': 'Uploaded file is not a zip file.'}, status=400)

        # Save the uploaded file to the file system
        fs = FileSystemStorage(location=FILE_SYSTEM_PATH)
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # Unzip the file
        with ZipFile(file_url, 'r') as zip_ref:
            zip_ref.extractall(FILE_SYSTEM_PATH)

        # Return success message
        return JsonResponse({'message': 'File has been successfully unzipped.', 'file_url': file_url})
    
    except Exception as e:
        # Handle any exceptions and return an error message
        return JsonResponse({'error': str(e)}, status=500)


# unzip_tool_app/urls.py"""
URL configuration for the Unzip Tool application.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('unzip/', views.unzip_file, name='unzip_file'),
]


# unzip_tool_app/apps.py"""
Application configuration for the Unzip Tool application.
"""
from django.apps import AppConfig

class UnzipToolAppConfig(AppConfig):
    name = 'unzip_tool_app'
    verbose_name = 'Unzip Tool'
