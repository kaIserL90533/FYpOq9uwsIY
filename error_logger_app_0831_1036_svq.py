# 代码生成时间: 2025-08-31 10:36:17
# error_logger_app/error_logger_app
# Django application for collecting error logs.

"""
This Django application provides functionality to collect and store error logs.
It follows Django's best practices and includes models, views, and URLs as required.
"""

import logging
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# Set up logger
logger = logging.getLogger(__name__)

# Create your models here.
class ErrorLog(models.Model):
    """Model to store error logs."""
    message = models.TextField(help_text="Error message")
    url = models.URLField(max_length=200, blank=True, null=True, help_text="URL where the error occurred")
    timestamp = models.DateTimeField(default=timezone.now, help_text="Timestamp of the error")

    def __str__(self):
        return self.message

# Create your views here.
@csrf_exempt
@require_http_methods(['POST'])
def log_error(request):
    """
    View to log errors. Accepts POST requests with error data and logs them.
    :param request: HttpRequest object containing error data.
    :return: JSON response indicating success or failure.
    """
    try:
        error_data = request.POST
        message = error_data.get('message', 'No message provided')
        url = error_data.get('url', '')
        timestamp = timezone.now()
        
        # Log error to database
        ErrorLog.objects.create(message=message, url=url, timestamp=timestamp)
        logger.error(f'Error logged: {message} at {url}')
        return JsonResponse({'status': 'success', 'message': 'Error logged successfully.'}, status=201)
    except Exception as e:
        logger.error(f'Failed to log error: {str(e)}')
        return JsonResponse({'status': 'error', 'message': 'Failed to log error.'}, status=500)

# Create your urls.py here.
urlpatterns = [
    path('log_error/', log_error, name='log_error'),
]
