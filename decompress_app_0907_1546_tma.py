# 代码生成时间: 2025-09-07 15:46:40
import zipfile
import os
from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.conf import settings

class DecompressView(View):
    """
    A view to handle the decompression of uploaded zip files.
    """
    def post(self, request):
        """
        Handle the POST request containing a zip file.
        Extracts the contents to a specified directory.
        """
        try:
            # Check if the file is in the request.FILES dictionary
            if 'zip_file' not in request.FILES:
                return JsonResponse({'error': 'No file provided'}, status=400)

            # Get the uploaded file
            zip_file = request.FILES['zip_file']
            if not zip_file.name.endswith('.zip'):
                return JsonResponse({'error': 'File must be a zip archive'}, status=400)

            # Get the path to save the extracted files
            extract_path = os.path.join(settings.MEDIA_ROOT, 'extracted')
            if not os.path.exists(extract_path):
                os.makedirs(extract_path)

            # Extract the zip file
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            # Return a successful response
            return JsonResponse({'message': 'File decompressed successfully'}, status=200)
        except zipfile.BadZipFile:
            return JsonResponse({'error': 'The provided file is not a valid zip archive'}, status=400)
        except Exception as e:
            # Log the exception here
            return JsonResponse({'error': 'An error occurred during decompression'}, status=500)

# URL configuration
urlpatterns = [
    path('decompress/', DecompressView.as_view(), name='decompress'),
]

# Note: This code assumes that the Django project settings include the following configurations:
#
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
