# 代码生成时间: 2025-10-11 22:03:51
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.files.storage import default_storage
import os
import magic
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import FileMetadata

class FileMetadataExtractor(View):
    """
    View to extract metadata from a file.
    """
    def get(self, request, *args, **kwargs):
        """
        Extract metadata for a given file.
        """
        try:
            file_id = request.GET.get('file_id')
            if not file_id:
                raise ValueError('File ID is required')
            
            file_storage = default_storage
            file_path = file_storage.path(file_id)
            if not file_storage.exists(file_id):
                raise FileNotFoundError('File does not exist')
            
            metadata = self.extract_metadata(file_path)
            return JsonResponse(metadata, safe=False)
        except (ValueError, FileNotFoundError) as e:
            return JsonResponse({'error': str(e)}, status=400)

    def extract_metadata(self, file_path):
        """
        Extract metadata from a file using python-magic library.
        """
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(file_path)
        
        metadata = {
            'name': os.path.basename(file_path),
            'size': os.path.getsize(file_path),
            'mime_type': mime_type
        }
        return metadata

# models.py
from django.db import models

class FileMetadata(models.Model):
    """
    Model to store file metadata.
    """
    file_id = models.CharField(max_length=255, unique=True, primary_key=True)
    metadata = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.file_id

    class Meta:
        verbose_name = 'File Metadata'
        verbose_name_plural = 'File Metadatas'

# urls.py
from django.urls import path
from .views import FileMetadataExtractor

urlpatterns = [
    path('extract/', FileMetadataExtractor.as_view(), name='extract_metadata'),
]
