# 代码生成时间: 2025-08-29 18:12:29
import os
import zipfile
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings

"""
A Django utility for unzipping uploaded zip files.
"""

class UnzipUtilityView(View):
    """
    A view to handle file uploads and unzipping.
    """

    @method_decorator(csrf_exempt, name='dispatch')
    @method_decorator(require_http_methods(['POST']), name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            # Get the uploaded file from the request
            uploaded_file = request.FILES.get('file', None)
            if not uploaded_file:
                return JsonResponse({'error': 'No file uploaded'}, status=400)

            # Ensure the uploaded file is a zip file
            if not uploaded_file.name.lower().endswith('.zip'):
                return JsonResponse({'error': 'Only zip files are allowed'}, status=400)

            # Create a path for the zip file in the MEDIA_ROOT
            zip_file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

            # Save the uploaded file
            with open(zip_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Unzip the file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(settings.MEDIA_ROOT)

            # Remove the zip file after extraction
            os.remove(zip_file_path)

            return JsonResponse({'message': 'File successfully unzipped'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

"""
URL configuration for the UnzipUtilityView.
"""
from django.urls import path

urlpatterns = [
    path('unzip/', UnzipUtilityView.as_view(), name='unzip_file'),
]
