# 代码生成时间: 2025-08-08 18:23:47
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO
from django.conf import settings
import os
import logging
import json

# Set up logging
logger = logging.getLogger(__name__)

class ImageResizerView(View):
    """
    A Django view to handle batch image resizing.
    
    This view takes a list of image file paths, resizes them according to the specified
    dimensions, and saves the resized images to a specified directory.
    
    Attributes:
        None
    
    Methods:
        get(request): Returns a simple GET response indicating the view is functional.
        post(request): Processes a POST request to resize images.
    """
    def get(self, request):
        """
        GET request handler.
        
        Returns a simple success message.
        """
        return JsonResponse({'message': 'Image Resizer View is functional.'})
    
    def post(self, request):
        """
        POST request handler.
        
        Processes a list of image file paths, resizes the images, and saves them.
        
        Args:
            request (HttpRequest): A Django HTTP request object.
            
        Returns:
            JsonResponse: A response containing the status of the operation.
        """
        # Check if the request contains the required data
        if 'images' not in request.POST or 'width' not in request.POST or 'height' not in request.POST:
            return JsonResponse({'error': 'Missing required parameters.'}, status=400)
        
        # Extract the list of image file paths and target dimensions
        image_paths = json.loads(request.POST['images'])
        width = int(request.POST['width'])
        height = int(request.POST['height'])
        
        # Define the target directory for resized images
        target_directory = os.path.join(settings.MEDIA_ROOT, 'resized_images')
        
        # Ensure the target directory exists
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        
        try:
            for image_path in image_paths:
                # Open the image file
                with Image.open(default_storage.path(image_path)) as img:
                    # Resize the image
                    img = img.resize((width, height), Image.ANTIALIAS)
                    
                    # Create the file name for the resized image
                    resized_image_name = os.path.join(
                        target_directory, 
                        os.path.basename(image_path).replace('.', '_resized.')
                    )
                    
                    # Save the resized image
                    resized_image_path = default_storage.save(resized_image_name, BytesIO())
                    img.save(default_storage.open(resized_image_path, 'wb'))
                    
            # Return success response
            return JsonResponse({'message': 'Images resized successfully.'})
        except Exception as e:
            # Log the exception
            logger.error(f'Error resizing images: {e}')
            # Return error response
            return JsonResponse({'error': 'Failed to resize images.'}, status=500)

# URL configuration for the image resizer view
from django.urls import path

urlpatterns = [
    path('resize/', ImageResizerView.as_view(), name='resize_images'),
]