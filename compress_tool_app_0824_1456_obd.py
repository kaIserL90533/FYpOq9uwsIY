# 代码生成时间: 2025-08-24 14:56:41
import zipfile
import os
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views import View
from django.urls import path
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
def compress_tool_app():
    """
    A Django app that provides a file compression and decompression tool.
    It allows users to upload compressed files and decompress them.
    It handles errors and provides responses in JSON format.
    """
    class DecompressView(View):
        """
        A view to handle file decompression.
        """
        @require_http_methods(['POST'])
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)
        
        def post(self, request):
            """
            Handles the POST request to decompress a file.
            """
            try:
                file = request.FILES.get('file')
                if not file:
                    return JsonResponse({'error': 'No file provided'}, status=400)

                filename = file._name
                if not filename.endswith('.zip'):
                    return JsonResponse({'error': 'Only zip files are supported'}, status=400)

                with zipfile.ZipFile(file) as zfile:
                    zfile.extractall(settings.MEDIA_ROOT)

                return JsonResponse({'message': 'File decompressed successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

    class CompressView(View):
        """
        A view to handle file compression.
        """
        @require_http_methods(['POST'])
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)
        
        def post(self, request):
            """
            Handles the POST request to compress a file.
            """
            try:
                # Get the list of files to compress
                files = request.POST.getlist('files[]')
                if not files:
                    return JsonResponse({'error': 'No files provided'}, status=400)

                # Check if files exist
                for file in files:
                    if not default_storage.exists(file):
                        return JsonResponse({'error': f'File {file} not found'}, status=400)

                # Create a new zip file
                zip_filename = 'compressed_file.zip'
                with zipfile.ZipFile(zip_filename, 'w') as zfile:
                    for file in files:
                        zfile.write(file, os.path.basename(file))

                # Save the zip file to the media root
                with open(zip_filename, 'rb') as zip_file:
                    default_storage.save(zip_filename, ContentFile(zip_file.read()))

                return JsonResponse({'message': 'File compressed successfully', 'filename': zip_filename})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

    # Define the URLs for the app
    urlpatterns = [
        path('decompress/', DecompressView.as_view(), name='decompress'),
        path('compress/', CompressView.as_view(), name='compress'),
    ]
