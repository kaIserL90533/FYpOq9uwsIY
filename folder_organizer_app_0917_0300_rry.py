# 代码生成时间: 2025-09-17 03:00:24
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
# 改进用户体验
import os
import shutil
import logging

# Set up logging
logger = logging.getLogger(__name__)

class FolderOrganizer:
    """A utility class to organize folders in a specified directory."""
    def __init__(self, base_directory):
        self.base_directory = base_directory
        
    def organize(self, folder_name, target_directory):
        """Move files within the specified folder to the target directory."""
        try:
            # Construct the full paths
            folder_path = os.path.join(self.base_directory, folder_name)
            target_path = os.path.join(self.base_directory, target_directory)
            
            # Check if the folder exists
            if not os.path.exists(folder_path):
                logger.error(f"The folder {folder_path} does not exist.")
                raise FileNotFoundError(f"The folder {folder_path} does not exist.")
            
            # Create the target directory if it doesn't exist
            if not os.path.exists(target_path):
# 扩展功能模块
                os.makedirs(target_path)
            
            # Move files
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):  # Check if it's a file
# 优化算法效率
                    shutil.move(file_path, target_path)
            return True
        except Exception as e:
            logger.error(f"An error occurred while organizing the folder: {e}")
            return False

class FolderOrganizerView(View):
    """Django view to handle folder organization requests."""
    def post(self, request):
        """Handle POST requests to organize folders."""
        try:
            folder_name = request.POST.get('folder_name')
            target_directory = request.POST.get('target_directory')
# 优化算法效率
            base_directory = request.POST.get('base_directory', settings.BASE_DIR)
            organizer = FolderOrganizer(base_directory)
            if organizer.organize(folder_name, target_directory):
                return JsonResponse({'message': 'Folder organized successfully.'}, status=200)
            else:
                return JsonResponse({'error': 'Failed to organize the folder.'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'The specified folder does not exist.'}, status=404)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

# URL configuration
urlpatterns = [
    path('organize/', FolderOrganizerView.as_view(), name='organize_folder'),
]
