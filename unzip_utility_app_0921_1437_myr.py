# 代码生成时间: 2025-09-21 14:37:24
# unzip_utility_app/models.py
def get_uncompressed_file_path(file_name):
    """
    Generate a unique file path for an uncompressed file.
    """
    import uuid
    return f"uncompressed/{uuid.uuid4().hex}/{file_name}"


def get_compressed_file_path(file_name):
    """
    Generate a unique file path for a compressed file.
    """
    import uuid
    return f"compressed/{uuid.uuid4().hex}/{file_name}"


# unzip_utility_app/views.py
def unzip_file(request):
    """
    Unzip a compressed file and save the uncompressed files.
    """
    from django.http import HttpResponse, JsonResponse
    from django.views.decorators.http import require_http_methods
    from django.core.files.storage import default_storage
    from zipfile import ZipFile
    import os
    
    @require_http_methods(["POST"])
    def view(request):
        try:
            # Handle file upload
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return JsonResponse({'error': 'No file provided'}, status=400)
            
            # Generate unique path for the compressed file
            compressed_file_path = get_compressed_file_path(uploaded_file.name)
            
            # Save the compressed file to the server
            default_storage.save(compressed_file_path, uploaded_file)
            
            # Check if the file is a zip archive
            if not uploaded_file.name.endswith('.zip'):
                return JsonResponse({'error': 'Unsupported file format'}, status=400)
            
            # Unzip the file
            uncompressed_file_path = get_uncompressed_file_path(uploaded_file.name)
            with ZipFile(uploaded_file, 'r') as zip_ref:
                zip_ref.extractall(uncompressed_file_path)
                
            # Return a success response
            return JsonResponse({'message': 'File unzipped successfully', 'path': uncompressed_file_path}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def archive_files(request):
    """
    Archive multiple files into a single zip file.
    """
    from django.http import HttpResponse, JsonResponse
    from django.views.decorators.http import require_http_methods
    from django.core.files.storage import default_storage
    from zipfile import ZipFile
    import os
    
    @require_http_methods(["POST"])
    def view(request):
        try:
            # Get the list of files from the request
            file_list = request.POST.getlist('files[]')
            
            # Generate unique path for the compressed file
            compressed_file_path = get_compressed_file_path('archive.zip')
            
            # Create a ZipFile object and add files
            with ZipFile(default_storage.path(compressed_file_path), 'w') as zip_ref:
                for file_name in file_list:
                    if not default_storage.exists(file_name):
                        return JsonResponse({'error': f'File {file_name} does not exist'}, status=404)
                    zip_ref.write(default_storage.path(file_name), arcname=os.path.basename(file_name))
                    
            # Return a success response
            return JsonResponse({'message': 'Files archived successfully', 'path': compressed_file_path}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# unzip_utility_app/urls.py
def get_urlpatterns():
    """
    Return a list of urlpatterns for the UnzipUtilityApp.
    """
    from django.urls import path
    from .views import unzip_file, archive_files
    
    return [
        path('unzip', unzip_file, name='unzip_file'),
        path('archive', archive_files, name='archive_files'),
    ]


# unzip_utility_app/apps.py
def ready(self):
    """
    Ready method for UnzipUtilityApp.
    """
    from django.apps import AppConfig
    from django.urls import include, path
    from .urls import get_urlpatterns
    
    self.urls = get_urlpatterns()
    
    return AppConfig.ready(self)